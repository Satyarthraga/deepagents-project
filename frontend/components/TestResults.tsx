"use client";
import { useState } from "react";

type Props = { passed: boolean; output: string };

export default function TestResults({ passed, output }: Props) {
  const [expanded, setExpanded] = useState(!passed);

  return (
    <div className={`border rounded-2xl overflow-hidden ${passed ? "border-green-800/50 bg-green-950/20" : "border-red-800/50 bg-red-950/20"}`}>
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full flex items-center justify-between px-4 py-3"
      >
        <div className="flex items-center gap-2">
          <span className={`text-sm font-semibold ${passed ? "text-green-400" : "text-red-400"}`}>
            {passed ? "✓ Compile passed" : "✗ Compile failed"}
          </span>
        </div>
        <span className="text-[#64748b] text-xs">{expanded ? "▲" : "▼"}</span>
      </button>

      {expanded && output && (
        <pre className="px-4 pb-4 text-xs font-mono text-[#94a3b8] overflow-auto max-h-48 scrollbar-thin whitespace-pre-wrap">
          {output}
        </pre>
      )}
    </div>
  );
}
