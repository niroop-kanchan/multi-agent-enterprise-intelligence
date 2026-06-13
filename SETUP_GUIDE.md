# 🤖 Multi-Agent Enterprise Intelligence System (MAEIS)
## Complete Step-by-Step Setup Guide

---

## ✅ SOFTWARE YOU NEED TO DOWNLOAD

| Software | What it is | Download Link | Notes |
|---|---|---|---|
| **Python 3.11** | Programming language | https://python.org/downloads | ✅ Already installed |
| **VS Code** | Code editor | https://code.visualstudio.com | ✅ Already installed |
| **Ollama** | Run AI models locally | https://ollama.com/download | 🔴 Must install |
| **Tesseract OCR** | Extract text from images | See Step 3 below | 🔴 Must install |
| **Git** (optional) | Version control | https://git-scm.com | Optional |

---

## STEP 1 — Install Ollama

### Windows
1. Go to https://ollama.com/download
2. Click **"Download for Windows"**
3. Run the `.exe` installer
4. After install, open **Command Prompt** and type:
```
ollama --version
```
You should see a version number like `ollama version 0.1.x`

### Mac
1. Go to https://ollama.com/download
2. Click **"Download for Mac"**
3. Open the `.dmg` and drag Ollama to Applications
4. Open Terminal and type:
```
ollama --version
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## STEP 2 — Pull the AI Model (Llama 3)

Open a terminal / command prompt and run:

```bash
ollama pull llama3
```

> ⚠️ This downloads ~4.7 GB. Wait for it to complete.  
> Alternative (smaller, 2 GB): `ollama pull gemma:2b`

Test the model works:
```bash
ollama run llama3 "Say hello in one sentence"
```

You should get a response. Type `/bye` to exit.

---

## STEP 3 — Install Tesseract OCR

### Windows
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Click the latest installer e.g. `tesseract-ocr-w64-setup-5.x.x.exe`
3. Run the installer — **IMPORTANT**: during install, check the box that says  
   **"Add Tesseract to the system PATH"**
4. Verify: open a NEW command prompt and type:
```
tesseract --version
```

### Mac
```bash
brew install tesseract
```
(Install Homebrew first from https://brew.sh if needed)

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr -y
```

---

## STEP 4 — Set Up the Project in VS Code

### 4.1 Extract the ZIP

1. Unzip `maeis.zip` to a folder of your choice  
   e.g. `C:\Projects\maeis` or `~/Projects/maeis`
2. Open VS Code
3. Go to **File → Open Folder** and select the `maeis` folder

### 4.2 Open the Integrated Terminal

Press **Ctrl + `** (backtick) or go to **Terminal → New Terminal**

### 4.3 Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

---

## STEP 5 — Install All Python Dependencies

Make sure your virtual environment is active, then run:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> ⏳ This will take 3–8 minutes. It downloads ~1.5 GB of packages.  
> Do NOT close the terminal.

---

## STEP 6 — Verify Everything Works

Run the setup test script:

```bash
python test_setup.py
```

Expected output (all green checkmarks):
```
✅ Python version OK
✅ streamlit
✅ crewai
✅ langchain_ollama
✅ chromadb
✅ pypdf
✅ pytesseract
✅ Pillow (PIL)
✅ sentence_transformers
✅ fpdf2 (fpdf)
✅ ollama SDK
✅ tesseract found in PATH
✅ Ollama running  |  models: ['llama3:latest']
✅ data/uploads
✅ data/reports
✅ data/chroma_db
```

---

## STEP 7 — Start the Application

### 7.1 Make sure Ollama is running

Open a **separate terminal window** and run:
```bash
ollama serve
```
Leave this window open in the background.

### 7.2 Launch the Streamlit app

In your VS Code terminal (with venv active):
```bash
streamlit run app.py
```

Your browser will open automatically at:  
**http://localhost:8501**

---

## STEP 8 — Using the Application

### 8.1 Upload & Process Tab
1. Click **"Browse files"** or drag and drop a PDF / image / text file
2. Click **"🚀 Run all agents"**
3. Watch the progress bar as all 5 agents work through your document
4. See the quick stats: word count, source type, knowledge base chunks

### 8.2 Results Tab
- **Summary** — Executive summary and key takeaways from the Summary Agent
- **Research Analysis** — Topics, entities, keywords, insights from the Research Agent
- **Extracted Raw Text** — Expandable view of the full extracted text
- **Download PDF Report** — Click to download the professional PDF report

### 8.3 Chat with Docs Tab
- Type any question about your uploaded documents
- The Chat Agent uses RAG to find relevant context and answer
- Expand "Source context" to see exactly which passages the agent used

### 8.4 Reports Tab
- View all generated PDF reports
- Download any report with one click

---

## 📁 Folder Structure Explained

```
maeis/
│
├── app.py                    ← Main Streamlit UI (entry point)
├── requirements.txt          ← All Python packages
├── test_setup.py             ← Pre-flight check script
├── .env                      ← Configuration (model name, paths)
│
├── agents/                   ← The 5 AI agents
│   ├── extraction_agent.py   ← Reads PDFs, images, text files
│   ├── research_agent.py     ← Analyses content for topics/entities
│   ├── summary_agent.py      ← Creates executive summaries
│   ├── report_agent.py       ← Generates PDF reports (fpdf2)
│   └── chat_agent.py         ← RAG-powered Q&A chatbot
│
├── core/                     ← Shared infrastructure
│   ├── llm.py                ← Ollama LLM wrapper (one place to change model)
│   └── knowledge_base.py     ← ChromaDB vector store manager
│
├── utils/
│   └── pipeline.py           ← Runs all 5 agents in sequence
│
├── config/
│   └── settings.py           ← Loads .env and sets constants
│
└── data/
    ├── uploads/              ← Saved uploaded files
    ├── reports/              ← Generated PDF reports
    └── chroma_db/            ← ChromaDB persistent vector database
```

---

## ❓ Common Errors & Fixes

### Error: "Ollama not running" / "Connection refused"
**Fix:** Open a new terminal and run `ollama serve`, leave it open.

### Error: "model 'llama3' not found"
**Fix:** Run `ollama pull llama3` and wait for it to finish.

### Error: "tesseract is not installed or not in PATH"
**Fix (Windows):** Reinstall Tesseract and make sure you check  
"Add to system PATH" during installation. Then restart VS Code.

### Error: "ModuleNotFoundError: No module named 'xyz'"
**Fix:** Make sure your venv is active (`venv\Scripts\activate`) then run  
`pip install -r requirements.txt` again.

### App is very slow
**Reason:** Llama 3 runs on CPU by default if you don't have a GPU.  
**Fix:** Switch to a smaller model: edit `.env` and set `OLLAMA_MODEL=gemma:2b`,  
then run `ollama pull gemma:2b`.

### ChromaDB error on first run
**Fix:** Delete the `data/chroma_db/` folder and restart the app.

---

## 🔧 Changing the AI Model

Edit the `.env` file:
```
OLLAMA_MODEL=gemma:2b
```
Available free models to try:
- `llama3` — Best quality (4.7 GB)
- `gemma:2b` — Fastest / smallest (1.4 GB)
- `mistral` — Good balance (4.1 GB)
- `phi3` — Microsoft's small model (2.3 GB)

Pull any model with: `ollama pull <model-name>`

---

## 🚀 What Makes This Resume-Worthy

This project demonstrates:
- **Multi-agent AI architecture** using real agent design patterns
- **RAG (Retrieval-Augmented Generation)** with ChromaDB vector search
- **Local LLM deployment** via Ollama (no API costs, no data leaks)
- **OCR pipeline** for image-to-text extraction
- **Professional PDF report generation** with fpdf2
- **Full-stack Python** — agents, vector DB, REST-like orchestration, web UI
- **Production patterns** — config management, error handling, session state

---

*Generated by MAEIS Setup Guide*
