"""
app.py  –  Multi-Agent Enterprise Intelligence System
======================================================
Run with:  streamlit run app.py
"""
import os
import sys
import streamlit as st

# ── Path setup ────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from core.knowledge_base import KnowledgeBase
from agents.chat_agent import ChatAgent
from utils.pipeline import run_pipeline
from config.settings import UPLOAD_DIR, REPORTS_DIR

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MAEIS – Multi-Agent Enterprise Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px 30px; border-radius: 12px; margin-bottom: 24px;
        color: white;
    }
    .main-header h1 { margin: 0; font-size: 2rem; }
    .main-header p  { margin: 4px 0 0; opacity: .8; font-size: .95rem; }

    .agent-card {
        background: #f8faff; border: 1px solid #d0dcf0;
        border-radius: 10px; padding: 16px; margin: 8px 0;
    }
    .agent-card h4 { color: #1e3c72; margin: 0 0 6px; }

    .stat-box {
        background: white; border: 1px solid #e0e8f8;
        border-radius: 8px; padding: 14px; text-align: center;
    }
    .stat-box .value { font-size: 1.6rem; font-weight: 700; color: #1e3c72; }
    .stat-box .label { font-size: .8rem; color: #666; margin-top: 2px; }

    .chat-user   { background:#e8f0fe; border-radius:12px; padding:10px 14px; margin:6px 0; }
    .chat-agent  { background:#f1f8e9; border-radius:12px; padding:10px 14px; margin:6px 0; }

    .success-banner {
        background:#e8f5e9; border-left:4px solid #43a047;
        padding:12px 16px; border-radius:6px; margin:10px 0;
    }
    .warning-banner {
        background:#fff8e1; border-left:4px solid #fb8c00;
        padding:12px 16px; border-radius:6px; margin:10px 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
if "kb" not in st.session_state:
    st.session_state.kb = KnowledgeBase()
if "chat_agent" not in st.session_state:
    st.session_state.chat_agent = ChatAgent(st.session_state.kb)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pipeline_results" not in st.session_state:
    st.session_state.pipeline_results = None
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

kb: KnowledgeBase = st.session_state.kb
chat_agent: ChatAgent = st.session_state.chat_agent

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="main-header">
  <h1>🤖 Multi-Agent Enterprise Intelligence System</h1>
  <p>Upload documents → AI agents analyse, summarise, and answer your questions — 100 % local & free</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ System Status")

    # Ollama check
    try:
        import ollama as _ollama
        _ollama.list()
        st.success("✅ Ollama  connected")
    except Exception:
        st.error("❌ Ollama  offline")
        st.info("Start Ollama: `ollama serve`\nThen pull model: `ollama pull llama3`")

    st.markdown(f"**Knowledge base:** `{kb.count()}` chunks")
    if st.button("🗑️ Clear knowledge base", use_container_width=True):
        kb.clear()
        st.session_state.chat_history = []
        st.session_state.processed_files = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 📂 Processed files")
    if st.session_state.processed_files:
        for f in st.session_state.processed_files:
            st.markdown(f"• `{f}`")
    else:
        st.markdown("_None yet_")

    st.markdown("---")
    st.markdown("### 🤖 Agents")
    for emoji, name, desc in [
        ("📄", "Extraction", "PDF, Image, Text"),
        ("🔍", "Research",   "Topics & entities"),
        ("📝", "Summary",    "Executive summary"),
        ("📊", "Report",     "PDF export"),
        ("💬", "Chat",       "RAG Q&A"),
    ]:
        st.markdown(f"{emoji} **{name}** — {desc}")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_upload, tab_results, tab_chat, tab_reports = st.tabs(
    ["📤 Upload & Process", "📋 Results", "💬 Chat with Docs", "📁 Reports"]
)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1  –  Upload & Process
# ══════════════════════════════════════════════════════════════════════════════
with tab_upload:
    st.markdown("### Upload a document")
    st.markdown(
        "Supported formats: **PDF**, **PNG / JPG / JPEG** (OCR), **TXT / MD / CSV**"
    )

    uploaded = st.file_uploader(
        "Choose a file",
        type=["pdf", "png", "jpg", "jpeg", "bmp", "tiff", "txt", "md", "csv"],
        label_visibility="collapsed",
    )

    if uploaded:
        # Save to uploads dir
        save_path = os.path.join(UPLOAD_DIR, uploaded.name)
        with open(save_path, "wb") as fh:
            fh.write(uploaded.getbuffer())

        col1, col2, col3 = st.columns(3)
        col1.metric("File", uploaded.name)
        col2.metric("Size", f"{uploaded.size / 1024:.1f} KB")
        col3.metric("Type", uploaded.type.split("/")[-1].upper())

        if st.button("🚀 Run all agents", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text  = st.empty()

            def update_progress(step, total, msg):
                progress_bar.progress(step / total)
                status_text.markdown(f"**{msg}**")

            with st.spinner("Processing…"):
                results = run_pipeline(save_path, kb, progress_cb=update_progress)

            progress_bar.progress(1.0)
            status_text.empty()

            if results["success"]:
                st.session_state.pipeline_results = results
                if uploaded.name not in st.session_state.processed_files:
                    st.session_state.processed_files.append(uploaded.name)
                st.markdown(
                    '<div class="success-banner">✅ All agents finished successfully! '
                    'Check the <b>Results</b> and <b>Chat</b> tabs.</div>',
                    unsafe_allow_html=True,
                )
                # Quick stats
                c1, c2, c3, c4 = st.columns(4)
                ext = results.get("extraction", {})
                rpt = results.get("report", {})
                c1.markdown(
                    f'<div class="stat-box"><div class="value">{ext.get("word_count",0):,}</div>'
                    f'<div class="label">Words extracted</div></div>',
                    unsafe_allow_html=True,
                )
                c2.markdown(
                    f'<div class="stat-box"><div class="value">{ext.get("source_type","—")}</div>'
                    f'<div class="label">Source type</div></div>',
                    unsafe_allow_html=True,
                )
                c3.markdown(
                    f'<div class="stat-box"><div class="value">{results.get("kb_chunks",0)}</div>'
                    f'<div class="label">KB chunks added</div></div>',
                    unsafe_allow_html=True,
                )
                c4.markdown(
                    f'<div class="stat-box"><div class="value">{"✅" if rpt.get("success") else "❌"}</div>'
                    f'<div class="label">Report generated</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.error(f"Pipeline failed: {results.get('error', 'Unknown error')}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2  –  Results
# ══════════════════════════════════════════════════════════════════════════════
with tab_results:
    res = st.session_state.pipeline_results
    if not res:
        st.info("No results yet. Upload and process a document first.")
    else:
        r_ext = res.get("extraction", {})
        r_res = res.get("research",  {})
        r_sum = res.get("summary",   {})
        r_rpt = res.get("report",    {})

        # Summary card
        st.markdown("### 📝 Summary")
        with st.container():
            st.markdown(
                f'<div class="agent-card">{r_sum.get("summary","—")}</div>',
                unsafe_allow_html=True,
            )

        # Research card
        st.markdown("### 🔍 Research Analysis")
        with st.container():
            st.markdown(
                f'<div class="agent-card">{r_res.get("analysis","—")}</div>',
                unsafe_allow_html=True,
            )

        # Raw text expander
        with st.expander("📄 Extracted raw text"):
            st.text_area(
                "Text",
                value=r_ext.get("text", ""),
                height=300,
                label_visibility="collapsed",
            )

        # Report download
        if r_rpt.get("success") and os.path.exists(r_rpt.get("report_path", "")):
            with open(r_rpt["report_path"], "rb") as fh:
                st.download_button(
                    "⬇️  Download PDF Report",
                    data=fh,
                    file_name=r_rpt["filename"],
                    mime="application/pdf",
                    use_container_width=True,
                )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3  –  Chat
# ══════════════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("### 💬 Chat with your documents")
    if kb.count() == 0:
        st.markdown(
            '<div class="warning-banner">⚠️ No documents in the knowledge base yet. '
            "Process a file first.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f"_Knowledge base contains **{kb.count()}** chunks from your documents._")

    # Chat history
    for msg in st.session_state.chat_history:
        css = "chat-user" if msg["role"] == "user" else "chat-agent"
        icon = "🧑" if msg["role"] == "user" else "🤖"
        st.markdown(
            f'<div class="{css}">{icon} {msg["content"]}</div>',
            unsafe_allow_html=True,
        )

    question = st.chat_input("Ask a question about your documents…")
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.spinner("Thinking…"):
            response = chat_agent.chat(question)
        answer = response["answer"]
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

        with st.expander("📚 Source context used by the agent"):
            for i, chunk in enumerate(response.get("context_chunks", []), 1):
                st.markdown(f"**Chunk {i}:** {chunk[:300]}…")

        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear chat history"):
            st.session_state.chat_history = []
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4  –  Reports
# ══════════════════════════════════════════════════════════════════════════════
with tab_reports:
    st.markdown("### 📁 Generated Reports")
    report_files = [
        f for f in os.listdir(REPORTS_DIR) if f.endswith(".pdf")
    ] if os.path.isdir(REPORTS_DIR) else []

    if not report_files:
        st.info("No reports generated yet.")
    else:
        st.markdown(f"Found **{len(report_files)}** report(s):")
        for rf in sorted(report_files, reverse=True):
            rpath = os.path.join(REPORTS_DIR, rf)
            size_kb = os.path.getsize(rpath) / 1024
            col_a, col_b = st.columns([4, 1])
            col_a.markdown(f"📄 `{rf}`  _{size_kb:.1f} KB_")
            with open(rpath, "rb") as fh:
                col_b.download_button(
                    "⬇️ Download",
                    data=fh,
                    file_name=rf,
                    mime="application/pdf",
                    key=f"dl_{rf}",
                )
