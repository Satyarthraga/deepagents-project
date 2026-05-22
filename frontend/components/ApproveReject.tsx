"use client";
import { useState } from "react";

type Props = {
  onApprove: () => void;
  onReject: (feedback: string) => void;
};

export default function ApproveReject({ onApprove, onReject }: Props) {
  const [mode, setMode] = useState<"idle" | "rejecting">("idle");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleApprove() {
    setLoading(true);
    await onApprove();
    setLoading(false);
  }

  async function handleReject() {
    if (!feedback.trim()) return;
    setLoading(true);
    await onReject(feedback);
    setLoading(false);
    setMode("idle");
    setFeedback("");
  }

  return (
    <div className="bg-[#1a1f2e] border border-orange-800/50 rounded-2xl p-4">
      <p className="text-orange-300 text-sm font-medium mb-1">⏸ Waiting for your review</p>
      <p className="text-[#64748b] text-xs mb-4">Review the diff above, then approve or provide feedback to revise.</p>

      {mode === "idle" ? (
        <div className="flex gap-3">
          <button
            onClick={handleApprove}
            disabled={loading}
            className="flex-1 bg-green-700 hover:bg-green-600 disabled:opacity-50 text-white text-sm font-semibold py-2.5 rounded-xl transition-colors"
          >
            {loading ? "..." : "✓ Approve & Commit"}
          </button>
          <button
            onClick={() => setMode("rejecting")}
            disabled={loading}
            className="flex-1 bg-[#2d3748] hover:bg-[#374151] disabled:opacity-50 text-[#94a3b8] text-sm font-semibold py-2.5 rounded-xl transition-colors"
          >
            ✗ Request Changes
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="Describe what needs to be fixed..."
            rows={3}
            className="w-full bg-[#0f1117] border border-[#2d3748] rounded-xl px-3 py-2 text-white placeholder-[#64748b] text-sm focus:outline-none focus:border-orange-500 resize-none"
          />
          <div className="flex gap-2">
            <button
              onClick={handleReject}
              disabled={loading || !feedback.trim()}
              className="flex-1 bg-orange-700 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-semibold py-2 rounded-xl transition-colors"
            >
              {loading ? "..." : "Send Feedback"}
            </button>
            <button
              onClick={() => setMode("idle")}
              className="px-4 text-[#64748b] hover:text-white text-sm rounded-xl hover:bg-[#2d3748] transition-colors"
            >
              Back
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
