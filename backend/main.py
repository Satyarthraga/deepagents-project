import asyncio
import json
import uuid
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.db import init_db, create_run, update_run, save_event, get_runs, get_events, get_run
from backend.agent import build_agent, git_diff, SERVICES, CLINICALOPS_ROOT

app = FastAPI(title="PRD-to-PR Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory state per run
_agents = {}           # run_id → agent instance
_approval_events = {}  # run_id → asyncio.Event
_run_tasks = {}        # run_id → asyncio.Task
_event_queues = {}     # run_id → asyncio.Queue
_run_services = {}     # run_id → service name (detected from agent run)


@app.on_event("startup")
def startup():
    init_db()


class RunRequest(BaseModel):
    prd_url: str | None = None
    prd_text: str | None = None


class ApproveRequest(BaseModel):
    pass


class RejectRequest(BaseModel):
    feedback: str


def _emit(run_id: str, type_: str, content):
    payload = {"type": type_, "content": content}
    save_event(run_id, type_, content)
    q = _event_queues.get(run_id)
    if q:
        asyncio.get_event_loop().call_soon_threadsafe(q.put_nowait, payload)


async def _run_agent(run_id: str, prd_input: str):
    try:
        agent = _agents[run_id]
        q = _event_queues[run_id]

        _emit(run_id, "step", "Agent started. Reading PRD...")

        config = {"configurable": {"thread_id": run_id}}
        messages = [{"role": "user", "content": f"Please process this PRD and implement the required changes:\n\n{prd_input}"}]

        async for chunk in agent.astream({"messages": messages}, config=config, stream_mode="updates"):
            for node, updates in chunk.items():
                if not updates or not isinstance(updates, dict) or "messages" not in updates:
                    continue
                for msg in updates["messages"]:
                    if hasattr(msg, "content") and msg.content and not hasattr(msg, "tool_calls"):
                        text = str(msg.content).strip()
                        if text:
                            _emit(run_id, "step", text[:500])
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            _emit(run_id, "tool", {"tool": tc["name"], "input": tc.get("args", {})})
                    if hasattr(msg, "name") and msg.name:
                        output = str(msg.content)[:1000] if hasattr(msg, "content") else ""
                        _emit(run_id, "tool_result", {"tool": msg.name, "output": output})
                        if msg.name == "compile_java_service":
                            passed = "[PASS]" in output
                            _emit(run_id, "compile", {"passed": passed, "output": output})
                        if msg.name == "create_pr":
                            urls = [w for w in output.split() if "github.com" in w and "/pull/" in w]
                            if urls:
                                update_run(run_id, pr_url=urls[0], status="done")
                                _emit(run_id, "pr", {"url": urls[0]})

            if "__interrupt__" in chunk:
                _emit(run_id, "waiting", {"message": "Changes ready — please review the diff and approve or reject."})
                update_run(run_id, status="waiting")
                event = asyncio.Event()
                _approval_events[run_id] = event
                await event.wait()
                _approval_events.pop(run_id, None)
                _emit(run_id, "step", "Approved. Continuing...")
                update_run(run_id, status="running")

        update_run(run_id, status="done")
        _emit(run_id, "done", {"summary": "Agent completed."})

    except Exception as e:
        update_run(run_id, status="failed")
        _emit(run_id, "error", {"message": str(e)})
    finally:
        q = _event_queues.get(run_id)
        if q:
            await q.put(None)


@app.post("/api/run")
async def start_run(req: RunRequest):
    prd_input = req.prd_url or req.prd_text
    if not prd_input:
        raise HTTPException(400, "Provide prd_url or prd_text")

    run_id = str(uuid.uuid4())
    create_run(run_id)

    _event_queues[run_id] = asyncio.Queue()
    _agents[run_id] = build_agent()

    task = asyncio.create_task(_run_agent(run_id, prd_input))
    _run_tasks[run_id] = task

    return {"run_id": run_id}


@app.get("/api/stream/{run_id}")
async def stream_run(run_id: str):
    run = get_run(run_id)
    if not run:
        raise HTTPException(404, "Run not found")

    async def event_stream() -> AsyncGenerator[str, None]:
        past_events = get_events(run_id)
        for ev in past_events:
            try:
                content = json.loads(ev["content"])
            except Exception:
                content = ev["content"]
            data = json.dumps({"type": ev["type"], "content": content})
            yield f"data: {data}\n\n"

        if run["status"] in ("done", "failed"):
            return

        q = _event_queues.get(run_id)
        if not q:
            return

        while True:
            event = await q.get()
            if event is None:
                break
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream",
                              headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.post("/api/approve/{run_id}")
async def approve_run(run_id: str):
    event = _approval_events.get(run_id)
    if not event:
        raise HTTPException(400, "No pending approval for this run")
    event.set()
    return {"status": "approved"}


@app.post("/api/reject/{run_id}")
async def reject_run(run_id: str, req: RejectRequest):
    run = get_run(run_id)
    if not run:
        raise HTTPException(404, "Run not found")

    save_event(run_id, "step", f"User rejected: {req.feedback}. Revising...")

    event = _approval_events.get(run_id)
    if event:
        q = _event_queues.get(run_id)
        if q:
            await q.put({"type": "step", "content": f"Feedback received: {req.feedback}. Revising changes..."})

        update_run(run_id, status="running")
        agent = _agents.get(run_id)
        if agent:
            config = {"configurable": {"thread_id": run_id}}
            messages = [{"role": "user", "content": f"The reviewer rejected the changes. Feedback: {req.feedback}\n\nPlease revise and fix the issues."}]
            task = asyncio.create_task(_run_agent_resume(run_id, agent, messages, config))
            _run_tasks[run_id] = task

        event.set()

    return {"status": "rejected"}


async def _run_agent_resume(run_id: str, agent, messages, config):
    try:
        async for chunk in agent.astream({"messages": messages}, config=config, stream_mode="updates"):
            for node, updates in chunk.items():
                if not updates or not isinstance(updates, dict) or "messages" not in updates:
                    continue
                for msg in updates["messages"]:
                    if hasattr(msg, "content") and msg.content and not hasattr(msg, "tool_calls"):
                        text = str(msg.content).strip()
                        if text:
                            _emit(run_id, "step", text[:500])
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            _emit(run_id, "tool", {"tool": tc["name"], "input": tc.get("args", {})})

            if "__interrupt__" in chunk:
                _emit(run_id, "waiting", {"message": "Changes revised — please review again."})
                update_run(run_id, status="waiting")
                event = asyncio.Event()
                _approval_events[run_id] = event
                await event.wait()
                _approval_events.pop(run_id, None)
                update_run(run_id, status="running")

        update_run(run_id, status="done")
        _emit(run_id, "done", {"summary": "Agent completed after revision."})
    except Exception as e:
        update_run(run_id, status="failed")
        _emit(run_id, "error", {"message": str(e)})
    finally:
        q = _event_queues.get(run_id)
        if q:
            await q.put(None)


@app.get("/api/runs")
async def list_runs():
    return get_runs()


@app.get("/api/diff/{run_id}")
async def get_diff(run_id: str):
    run = get_run(run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    service = run.get("service")
    if not service or service not in SERVICES:
        all_diffs = []
        for svc in SERVICES:
            svc_path = CLINICALOPS_ROOT / SERVICES[svc]
            if svc_path.exists():
                import subprocess
                result = subprocess.run("git diff HEAD 2>/dev/null || git diff",
                                        shell=True, cwd=svc_path, capture_output=True, text=True)
                if result.stdout.strip():
                    all_diffs.append(f"=== {svc} ===\n{result.stdout}")
        return {"diff": "\n".join(all_diffs) or "No changes detected."}
    return {"diff": git_diff(service)}
