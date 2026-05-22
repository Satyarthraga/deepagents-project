"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  const [mode, setMode] = useState<"url" | "text">("url");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;
    setLoading(true);
    setError("");
    try {
      const body = mode === "url" ? { prd_url: input } : { prd_text: input };
      const res = await fetch("http://localhost:8000/api/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(await res.text());
      const { run_id } = await res.json();
      router.push(`/runs/${run_id}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
      setLoading(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-20">
      <div className="mb-12 text-center">
        <h1 className="text-4xl font-bold text-white mb-3">PRD → PR</h1>
        <p className="text-[#64748b] text-lg">Paste a PRD and the agent will implement it and open a GitHub PR.</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-[#1a1f2e] rounded-2xl border border-[#2d3748] p-6">
        <div className="flex gap-2 mb-5">
          {(["url", "text"] as const).map((m) => (
            <button
              key={m}
              type="button"
              onClick={() => setMode(m)}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                mode === m
                  ? "bg-indigo-600 text-white"
                  : "text-[#64748b] hover:text-white hover:bg-[#2d3748]"
              }`}
            >
              {m === "url" ? "Google Docs / Notion URL" : "Paste PRD text"}
            </button>
          ))}
        </div>

        {mode === "url" ? (
          <input
            type="url"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="https://docs.google.com/document/d/..."
            className="w-full bg-[#0f1117] border border-[#2d3748] rounded-xl px-4 py-3 text-white placeholder-[#64748b] focus:outline-none focus:border-indigo-500 text-sm"
          />
        ) : (
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Paste the PRD content here..."
            rows={10}
            className="w-full bg-[#0f1117] border border-[#2d3748] rounded-xl px-4 py-3 text-white placeholder-[#64748b] focus:outline-none focus:border-indigo-500 text-sm resize-none font-mono"
          />
        )}

        {error && (
          <p className="mt-3 text-red-400 text-sm">{error}</p>
        )}

        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="mt-4 w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Starting agent...
            </>
          ) : (
            "Run Agent"
          )}
        </button>
      </form>

      <div className="mt-6 text-center">
        <a href="/history" className="text-[#64748b] hover:text-indigo-400 text-sm transition-colors">
          View PR history →
        </a>
      </div>
    </div>
  );
}
