import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ClinicalOps Agent",
  description: "PRD-to-PR coding agent for ClinicalOps",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col bg-[#0f1117] text-[#e2e8f0]">
        <nav className="border-b border-[#2d3748] px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-sm font-bold">C</div>
            <span className="font-semibold text-white">ClinicalOps Agent</span>
          </div>
          <div className="flex gap-6 text-sm text-[#64748b]">
            <a href="/" className="hover:text-white transition-colors">New Run</a>
            <a href="/history" className="hover:text-white transition-colors">History</a>
          </div>
        </nav>
        <main className="flex-1">{children}</main>
      </body>
    </html>
  );
}
