"use client";
import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import DiffViewer from "@/components/DiffViewer";
import ApproveReject from "@/components/ApproveReject";
import TestResults from "@/components/TestResults";

type Event = {
  type: string;
  content: unknown;
};

const ICONS: Record<string, string> = {
  step: "→",
  tool: "⚙",
  tool_result: "✓",
  compile: "🔨",
  waiting: "⏸",
  pr: "🔗",
  done: "✅",
  error: "✗",
};

const COLORS: Record<string, string> = {
  step: "text-[#94a3b8]",
  tool: "text-indigo-400",
  tool_result: "text-[#64748b]",
  compile: "text-yellow-400",
  waiting: "text-orange-400",
  pr: "text-green-400",
  done: "text-green-400",
  error: "text-red-400",
};

function formatContent(ev: Event): string {
  if (typeof ev.content === "string") return ev.content;
  if (typeof ev.content === "object" && ev.content !== null) {
    const c = ev.content as Record<string, unknown>;
    if (ev.type === "tool") return `${c.tool}(${JSON.stringify(c.input ?? {}).slice(0, 120)})`;
    if (ev.type === "tool_result") return `${c.tool} → ${String(c.output ?? "").slice(0, 200)}`;
    if (ev.type === "compile") return `Compile ${(c.passed ? "PASSED" : "FAILED")}`;
    if (ev.type === "pr") return `PR created: ${c.url}`;
    if (ev.type === "done") return String(c.summary ?? "Done");
    if (ev.type === "error") return String(c.message ?? "Error");
    if (ev.type === "waiting") return String(c.message ?? "Waiting for approval");
    return JSON.stringify(ev.content).slice(0, 200);
  }
  return String(ev.content);
}

export default function RunPage() {
  const { id } = useParams<{ id: string }>();
  const [events, setEvents] = useState<Event[]>([]);
  const [status, setStatus] = useState<"running" | "waiting" | "done" | "failed">("running");
  const [diff, setDiff] = useState("");
  const [compileResult, setCompileResult] = useState<{ passed: boolean; output: string } | null>(null);
  const [prUrl, setPrUrl] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const esRef = useRef<EventSource | null>(null);

  useEffect(() => {
    const es = new EventSource(`http://localhost:8000/api/stream/${id}`);
    esRef.current = es;

    es.onmessage = (e) => {
      const ev: Event = JSON.parse(e.data);
      setEvents((prev) => [...prev, ev]);

      if (ev.type === "waiting") {
        setStatus("waiting");
        fetch(`http://localhost:8000/api/diff/${id}`)
          .then((r) => r.json())
          .then((d) => setDiff(d.diff || ""));
      }
      if (ev.type === "compile") {
        const c = ev.content as { passed: boolean; output: string };
        setCompileResult(c);
      }
      if (ev.type === "pr") {
        const c = ev.content as { url: string };
        setPrUrl(c.url);
        setStatus("done");
      }
      if (ev.type === "done") setStatus("done");
      if (ev.type === "error") setStatus("failed");
    };

    return () => es.close();
  }, [id]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [events]);

  async function handleApprove() {
    await fetch(`http://localhost:8000/api/approve/${id}`, { method: "POST" });
    setStatus("running");
    setDiff("");
  }

  async function handleReject(feedback: string) {
    await fetch(`http://localhost:8000/api/reject/${id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ feedback }),
    });
    setStatus("running");
    setDiff("");
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-8 flex gap-6">
      {/* Left: event stream */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-3 mb-6">
          <h1 className="text-lg font-semibold text-white">Agent Run</h1>
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
            status === "running" ? "bg-indigo-900 text-indigo-300" :
            status === "waiting" ? "bg-orange-900 text-orange-300" :
            status === "done" ? "bg-green-900 text-green-300" :
            "bg-red-900 text-red-300"
          }`}>
            {status === "running" && <span className="inline-block w-2 h-2 rounded-full bg-indigo-400 animate-pulse mr-1.5" />}
            {status}
          </span>
          <span className="text-[#64748b] text-xs font-mono">{id}</span>
        </div>

        <div className="bg-[#1a1f2e] rounded-2xl border border-[#2d3748] p-4 h-[60vh] overflow-y-auto scrollbar-thin font-mono text-sm space-y-1">
          {events.map((ev, i) => (
            <div key={i} className={`flex gap-2 ${COLORS[ev.type] || "text-[#94a3b8]"}`}>
              <span className="shrink-0 w-4 text-center opacity-60">{ICONS[ev.type] || "·"}</span>
              <span className="break-all leading-relaxed">{formatContent(ev)}</span>
            </div>
          ))}
          {status === "running" && (
            <div className="flex gap-2 text-[#64748b]">
              <span className="w-4 text-center">·</span>
              <span className="animate-pulse">Working...</span>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Compile results */}
        {compileResult && (
          <div className="mt-4">
            <TestResults passed={compileResult.passed} output={compileResult.output} />
          </div>
        )}

        {/* PR link */}
        {prUrl && (
          <div className="mt-4 bg-green-950 border border-green-800 rounded-xl p-4 flex items-center justify-between">
            <div>
              <p className="text-green-400 font-semibold text-sm">PR Created</p>
              <a href={prUrl} target="_blank" rel="noopener noreferrer"
                 className="text-green-300 hover:text-green-200 text-sm underline break-all">
                {prUrl}
              </a>
            </div>
            <a href={prUrl} target="_blank" rel="noopener noreferrer"
               className="ml-4 shrink-0 bg-green-700 hover:bg-green-600 text-white text-sm px-4 py-2 rounded-lg transition-colors">
              Open PR →
            </a>
          </div>
        )}
      </div>

      {/* Right: diff + approve/reject */}
      {status === "waiting" && (
        <div className="w-[420px] shrink-0 space-y-4">
          <DiffViewer diff={diff} />
          <ApproveReject onApprove={handleApprove} onReject={handleReject} />
        </div>
      )}
    </div>
  );
}
