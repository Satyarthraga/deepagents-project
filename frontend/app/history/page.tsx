"use client";
import { useEffect, useState } from "react";

type Run = {
  id: string;
  prd_summary: string | null;
  service: string | null;
  branch: string | null;
  status: string;
  pr_url: string | null;
  created_at: string;
};

const STATUS_STYLES: Record<string, string> = {
  done: "bg-green-900 text-green-300",
  running: "bg-indigo-900 text-indigo-300",
  waiting: "bg-orange-900 text-orange-300",
  failed: "bg-red-900 text-red-300",
};

export default function HistoryPage() {
  const [runs, setRuns] = useState<Run[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/runs")
      .then((r) => r.json())
      .then((data) => { setRuns(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-bold text-white mb-8">PR History</h1>

      {loading ? (
        <div className="text-[#64748b] text-sm">Loading...</div>
      ) : runs.length === 0 ? (
        <div className="text-center py-20 text-[#64748b]">
          <p className="text-4xl mb-3">📭</p>
          <p>No runs yet. <a href="/" className="text-indigo-400 hover:underline">Start your first run →</a></p>
        </div>
      ) : (
        <div className="space-y-3">
          {runs.map((run) => (
            <div key={run.id}
                 className="bg-[#1a1f2e] border border-[#2d3748] rounded-xl p-4 flex items-center gap-4 hover:border-[#4a5568] transition-colors">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${STATUS_STYLES[run.status] || "bg-[#2d3748] text-[#94a3b8]"}`}>
                    {run.status}
                  </span>
                  {run.service && (
                    <span className="text-xs bg-[#2d3748] text-[#94a3b8] px-2 py-0.5 rounded-full">
                      {run.service}
                    </span>
                  )}
                  <span className="text-xs text-[#64748b]">{new Date(run.created_at).toLocaleString()}</span>
                </div>
                <p className="text-sm text-white truncate">{run.prd_summary || "No summary"}</p>
                {run.branch && (
                  <p className="text-xs text-[#64748b] mt-0.5 font-mono">{run.branch}</p>
                )}
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <a href={`/runs/${run.id}`}
                   className="text-xs text-[#64748b] hover:text-indigo-400 transition-colors px-3 py-1.5 rounded-lg hover:bg-[#2d3748]">
                  View
                </a>
                {run.pr_url && (
                  <a href={run.pr_url} target="_blank" rel="noopener noreferrer"
                     className="text-xs bg-indigo-900 text-indigo-300 hover:bg-indigo-800 px-3 py-1.5 rounded-lg transition-colors">
                    Open PR →
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
