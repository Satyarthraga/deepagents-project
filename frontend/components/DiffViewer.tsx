"use client";
import { useState } from "react";

type Props = { diff: string };

function parseDiff(diff: string) {
  if (!diff.trim()) return [];
  const lines = diff.split("\n");
  return lines.map((line, i) => {
    let cls = "text-[#64748b]";
    if (line.startsWith("+++") || line.startsWith("---")) cls = "text-[#64748b] font-bold";
    else if (line.startsWith("@@")) cls = "text-indigo-400 bg-indigo-950/30";
    else if (line.startsWith("+")) cls = "text-green-400 bg-green-950/20";
    else if (line.startsWith("-")) cls = "text-red-400 bg-red-950/20";
    return { line, cls, key: i };
  });
}

export default function DiffViewer({ diff }: Props) {
  const [expanded, setExpanded] = useState(true);
  const lines = parseDiff(diff);

  return (
    <div className="bg-[#1a1f2e] border border-[#2d3748] rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-white hover:bg-[#2d3748] transition-colors"
      >
        <span>📄 Changes ({lines.filter(l => l.line.startsWith("+") && !l.line.startsWith("+++")).length} additions, {lines.filter(l => l.line.startsWith("-") && !l.line.startsWith("---")).length} deletions)</span>
        <span className="text-[#64748b]">{expanded ? "▲" : "▼"}</span>
      </button>

      {expanded && (
        <div className="overflow-auto max-h-[50vh] scrollbar-thin">
          {diff.trim() ? (
            <pre className="text-xs font-mono px-4 pb-4 leading-5">
              {lines.map(({ line, cls, key }) => (
                <div key={key} className={`${cls} px-1 rounded-sm`}>{line || " "}</div>
              ))}
            </pre>
          ) : (
            <div className="px-4 pb-4 text-[#64748b] text-sm">No diff available yet.</div>
          )}
        </div>
      )}
    </div>
  );
}
