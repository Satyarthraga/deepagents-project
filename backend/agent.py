import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from deepagents import create_deep_agent

load_dotenv(Path(__file__).parent.parent / ".env")

CLINICALOPS_ROOT = Path("/Users/diwakarpatel/Documents/ragaai/clinicalops-setup")

SERVICES = {
    "auth":           "services/clinicalops-auth-service",
    "gateway":        "services/clinicalops-gateway-service",
    "internal-api":   "services/clinicalops-internal-api",
    "workflow":       "services/clinicalops-workflow-service",
    "document":       "services/clinicalops-document-service",
    "db-migration":   "services/clinicalops-db-migration",
    "rpa-collection": "clinicalops-rpa-collection",
}

SKIP_DIRS = {".git", "target", ".venv", "node_modules", "__pycache__", ".mvn"}


def _service_path(service: str) -> Path:
    rel = SERVICES.get(service)
    if not rel:
        raise ValueError(f"Unknown service '{service}'. Choose from: {list(SERVICES)}")
    return CLINICALOPS_ROOT / rel


def _run(cmd: str, cwd: Path, timeout: int = 120) -> str:
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
        output = (result.stdout + result.stderr).strip()
        return output[:4000] if len(output) > 4000 else output
    except subprocess.TimeoutExpired:
        return f"Error: command timed out after {timeout}s"
    except Exception as e:
        return f"Error: {e}"


def fetch_prd(url: str) -> str:
    """Fetch a PRD from a Google Docs or Notion URL, or return text as-is if not a URL."""
    import requests
    if not url.startswith("http"):
        return url
    if "docs.google.com" in url:
        doc_id = None
        for part in url.split("/"):
            if len(part) > 20 and part.replace("-", "").replace("_", "").isalnum():
                doc_id = part
        if doc_id:
            export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
            resp = requests.get(export_url, timeout=15)
            if resp.ok:
                return resp.text
    try:
        resp = requests.get(url, timeout=15)
        return resp.text[:8000]
    except Exception as e:
        return f"Error fetching PRD: {e}"


def list_service_files(service: str, pattern: str = "") -> str:
    """List files in a service. service: auth|gateway|internal-api|workflow|document|db-migration|rpa-collection"""
    root = _service_path(service)
    if not root.exists():
        return f"Service directory not found: {root}. Run 'make setup' in clinicalops-setup first."
    files = []
    for f in sorted(root.rglob("*")):
        if any(skip in f.parts for skip in SKIP_DIRS):
            continue
        if not f.is_file():
            continue
        rel = str(f.relative_to(root))
        if pattern and pattern not in rel:
            continue
        files.append(rel)
    return "\n".join(files[:200]) if files else "No files found."


def read_service_file(service: str, path: str) -> str:
    """Read a file from a service. path is relative to the service root."""
    root = _service_path(service)
    target = (root / path).resolve()
    if not str(target).startswith(str(root.resolve())):
        return "Error: path is outside service directory."
    if not target.exists():
        return f"Error: file not found: {path}"
    try:
        content = target.read_text(encoding="utf-8")
        return content[:6000] if len(content) > 6000 else content
    except Exception as e:
        return f"Error reading file: {e}"


def search_service(service: str, query: str, file_type: str = "") -> str:
    """Search for a string in a service. file_type: java|py|sql|yml|xml|properties"""
    root = _service_path(service)
    include = f"--include='*.{file_type}'" if file_type else \
              "--include='*.java' --include='*.py' --include='*.sql' --include='*.yml' --include='*.xml' --include='*.properties'"
    cmd = f"grep -r {include} -l '{query}' . 2>/dev/null | head -20"
    result = _run(cmd, root)
    if not result:
        return f"No matches found for '{query}' in {service}."
    lines = []
    for filepath in result.strip().splitlines():
        ctx = _run(f"grep -n '{query}' '{filepath}' | head -5", root)
        lines.append(f"--- {filepath} ---\n{ctx}")
    return "\n\n".join(lines)


def write_service_file(service: str, path: str, content: str) -> str:
    """Create or overwrite a file in a service. path is relative to service root."""
    root = _service_path(service)
    target = (root / path).resolve()
    if not str(target).startswith(str(root.resolve())):
        return "Error: path is outside service directory."
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Written: {path}"


def edit_service_file(service: str, path: str, old_str: str, new_str: str) -> str:
    """Make a targeted string replacement in a service file."""
    root = _service_path(service)
    target = (root / path).resolve()
    if not str(target).startswith(str(root.resolve())):
        return "Error: path is outside service directory."
    if not target.exists():
        return f"Error: file not found: {path}"
    content = target.read_text(encoding="utf-8")
    if old_str not in content:
        return f"Error: string not found in {path}."
    target.write_text(content.replace(old_str, new_str, 1), encoding="utf-8")
    return f"Edited: {path}"


def compile_java_service(service: str) -> str:
    """Compile a Java service to validate changes. Returns PASS or FAIL with output."""
    root = _service_path(service)
    if not (root / "pom.xml").exists():
        return f"Not a Maven project: {service}"
    result = _run("./mvnw compile -q 2>&1 | tail -20", root, timeout=180)
    passed = "ERROR" not in result and "BUILD FAILURE" not in result
    status = "PASS" if passed else "FAIL"
    return f"[{status}]\n{result}"


def sync_rpa(rpa_name: str) -> str:
    """Run uv sync for an RPA to validate Python dependencies."""
    rpa_dir = CLINICALOPS_ROOT / "clinicalops-rpa-collection" / "rpas" / rpa_name
    if not rpa_dir.exists():
        return f"RPA not found: {rpa_name}"
    return _run("uv sync -q 2>&1", rpa_dir, timeout=60)


def git_create_branch(service: str, branch_name: str) -> str:
    """Create a new git branch in a service repo."""
    root = _service_path(service)
    safe_name = branch_name.replace(" ", "-").lower()
    return _run(f"git checkout -b feature/prd-{safe_name} 2>&1", root)


def git_status(service: str) -> str:
    """Show git status for a service repo."""
    return _run("git status --short", _service_path(service))


def git_diff(service: str) -> str:
    """Show git diff (staged + unstaged) for a service repo."""
    root = _service_path(service)
    return _run("git diff HEAD 2>/dev/null || git diff", root)


def git_commit(service: str, message: str) -> str:
    """Stage all changes and commit in a service repo."""
    root = _service_path(service)
    return _run(f'git add -A && git commit -m "{message}"', root)


def git_push(service: str) -> str:
    """Push current branch to remote in a service repo."""
    return _run("git push -u origin HEAD 2>&1", _service_path(service))


def create_pr(service: str, title: str, body: str) -> str:
    """Create a GitHub PR for a service repo using gh CLI."""
    root = _service_path(service)
    safe_body = body.replace('"', '\\"')
    return _run(f'gh pr create --title "{title}" --body "{safe_body}" 2>&1', root)


SYSTEM_PROMPT = """You are a coding agent for the ClinicalOps platform — a healthcare microservices system.

Your job: read a PRD, identify which service(s) need changes, implement them, compile to validate, then create a GitHub PR.

Services available:
- auth          → Spring Boot auth service (JWT, port 8081)
- gateway       → Spring Boot API gateway (port 8082)
- internal-api  → Spring Boot core domain APIs (port 8083)
- workflow      → Spring Boot + Temporal workflow service (port 8085)
- document      → Spring Boot document management (port 8080)
- db-migration  → Flyway SQL migrations + Python data migrations
- rpa-collection → Python RPAs (Playwright-based automation agents)

Workflow:
1. fetch_prd → read and understand requirements
2. list_service_files + search_service + read_service_file → understand existing patterns
3. Plan your changes (think before writing)
4. git_create_branch → create feature branch
5. write_service_file / edit_service_file → implement changes
6. compile_java_service (for Java) or sync_rpa (for Python) → validate
7. If compile fails → fix and re-compile
8. git_status + git_diff → confirm what changed
9. STOP and wait for human review (human-in-the-loop checkpoint)
10. After approval: git_commit → git_push → create_pr

Rules:
- Always read existing code before writing new code
- Follow existing patterns (package names, naming conventions, imports)
- For Spring Boot: place files in correct package under src/main/java
- Never commit secrets or env vars
- Write concise commit messages
- PR body must include: what changed, why, and list of modified files"""


def build_agent():
    from langgraph.checkpoint.memory import MemorySaver

    model = ChatOpenAI(
        model="kimi-k2.6",
        base_url="https://api.moonshot.ai/v1",
        api_key=os.environ["MOONSHOT_API_KEY"],
        extra_body={"thinking": {"type": "disabled"}},
    )

    tools = [
        fetch_prd,
        list_service_files,
        read_service_file,
        search_service,
        write_service_file,
        edit_service_file,
        compile_java_service,
        sync_rpa,
        git_create_branch,
        git_status,
        git_diff,
        git_commit,
        git_push,
        create_pr,
    ]

    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=MemorySaver(),
    )
