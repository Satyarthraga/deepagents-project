import os
from pathlib import Path
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

CLINICALOPS_ROOT = Path("/Users/diwakarpatel/Documents/ragaai/clinicalops-setup")


def list_project_files() -> str:
    """List all files in the clinicalops-setup project."""
    files = [
        str(f.relative_to(CLINICALOPS_ROOT))
        for f in sorted(CLINICALOPS_ROOT.rglob("*"))
        if f.is_file() and not any(p.startswith(".") for p in f.parts[len(CLINICALOPS_ROOT.parts):])
    ]
    return "\n".join(files) if files else "No files found."


def read_project_file(path: str) -> str:
    """Read a file from the clinicalops-setup project. Path is relative to the project root."""
    target = (CLINICALOPS_ROOT / path).resolve()
    if not str(target).startswith(str(CLINICALOPS_ROOT.resolve())):
        return "Error: Path is outside the allowed directory."
    if not target.exists():
        return f"Error: File not found: {path}"
    try:
        return target.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"


tools = [DuckDuckGoSearchRun(), list_project_files, read_project_file]


def build_model():
    provider = os.environ.get("DEEP_AGENT_PROVIDER", "kimi")

    if provider == "kimi":
        return ChatOpenAI(
            model="kimi-k2.6",
            base_url="https://api.moonshot.ai/v1",
            api_key=os.environ["MOONSHOT_API_KEY"],
            extra_body={"thinking": {"type": "disabled"}},
        )

    if provider == "openai":
        return ChatOpenAI(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
            api_key=os.environ["OPENAI_API_KEY"],
        )

    if provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=os.environ.get("GOOGLE_MODEL", "gemini-2.0-flash"),
            google_api_key=os.environ["GOOGLE_API_KEY"],
        )

    raise ValueError(f"Unknown DEEP_AGENT_PROVIDER: {provider!r}. Choose: kimi, openai, google")


agent = create_deep_agent(
    model=build_model(),
    tools=tools,
    system_prompt="You are an expert researcher and assistant with read-only access to the clinicalops-setup project files.",
)


def run(query: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) or "What is LangGraph?"
    print(run(query))
