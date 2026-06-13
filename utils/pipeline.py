"""
utils/pipeline.py
------------------
Orchestrates the full multi-agent pipeline:
  1. ExtractionAgent  → raw text
  2. ResearchAgent    → analysis
  3. SummaryAgent     → summaries
  4. ReportAgent      → PDF report
  5. KnowledgeBase    → store chunks for RAG
"""
import os
from agents import ExtractionAgent, ResearchAgent, SummaryAgent, ReportAgent
from core.knowledge_base import KnowledgeBase
from config.settings import UPLOAD_DIR


def run_pipeline(file_path: str, kb: KnowledgeBase, progress_cb=None) -> dict:
    """
    Run all agents on the given file.

    progress_cb(step: int, total: int, message: str) is called at each step
    so the UI can update a progress bar.
    """
    total_steps = 5
    results = {}

    def _cb(step, msg):
        if progress_cb:
            progress_cb(step, total_steps, msg)

    # ── Step 1: Extraction ───────────────────────────────────────────────
    _cb(1, "📄 Extracting document text…")
    extraction = ExtractionAgent().run(file_path)
    results["extraction"] = extraction
    if not extraction["success"]:
        return {"success": False, "error": extraction.get("error", "Extraction failed"), **results}

    text = extraction["text"]

    # ── Step 2: Research ─────────────────────────────────────────────────
    _cb(2, "🔍 Running research analysis…")
    research = ResearchAgent().run(text)
    results["research"] = research

    # ── Step 3: Summary ──────────────────────────────────────────────────
    _cb(3, "📝 Generating summaries…")
    summary = SummaryAgent().run(text)
    results["summary"] = summary

    # ── Step 4: Report ───────────────────────────────────────────────────
    _cb(4, "📊 Creating PDF report…")
    report = ReportAgent().run(
        filename=extraction["filename"],
        extraction_result=extraction,
        research_result=research,
        summary_result=summary,
    )
    results["report"] = report

    # ── Step 5: Knowledge base ───────────────────────────────────────────
    _cb(5, "🧠 Storing in knowledge base…")
    chunks_added = kb.add_document(
        text,
        metadata={"filename": extraction["filename"], "source_type": extraction["source_type"]},
    )
    results["kb_chunks"] = chunks_added

    return {"success": True, **results}
