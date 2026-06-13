# MAEIS - Multi-Agent Enterprise Intelligence System

## Overview

MAEIS (Multi-Agent Enterprise Intelligence System) is an AI-powered enterprise document intelligence platform that automates document processing, analysis, summarization, and knowledge retrieval using local Large Language Models (LLMs).

The system uses OCR, Retrieval-Augmented Generation (RAG), Vector Databases, and Multi-Agent workflows to transform unstructured business documents into actionable insights.

---

## Features

### Document Processing

* PDF document ingestion
* Image document ingestion
* OCR text extraction using Tesseract
* Text file support

### AI-Powered Analysis

* Executive summaries
* Research analysis
* Topic extraction
* Key insight generation

### Enterprise Knowledge Base

* ChromaDB vector database
* Semantic search
* Persistent document memory

### Conversational AI

* Chat with uploaded documents
* Context-aware responses
* Retrieval-Augmented Generation (RAG)

### Report Generation

* Professional PDF reports
* Downloadable analysis reports

### Local AI Deployment

* Runs completely offline
* Powered by Ollama
* No OpenAI API costs
* Privacy-friendly architecture

---

## Architecture

```text
Document Upload
       │
       ▼
Extraction Agent
       │
       ▼
Research Agent
       │
       ▼
Summary Agent
       │
       ▼
Report Agent
       │
       ▼
Chat Agent (RAG)
       │
       ▼
Streamlit Dashboard
```

---

## Technology Stack

### AI & LLMs

* Ollama
* Llama 3
* LangChain

### Vector Database

* ChromaDB

### OCR

* Tesseract OCR
* PyTesseract

### Document Processing

* PyPDF

### Frontend

* Streamlit

### Embeddings

* Sentence Transformers

### Reporting

* FPDF2

### Programming Language

* Python 3.11

---

## Project Structure

```text
maeis/
│
├── app.py
├── requirements.txt
├── test_setup.py
│
├── agents/
│   ├── extraction_agent.py
│   ├── research_agent.py
│   ├── summary_agent.py
│   ├── report_agent.py
│   └── chat_agent.py
│
├── core/
│   ├── llm.py
│   └── knowledge_base.py
│
├── config/
│   └── settings.py
│
├── utils/
│   └── pipeline.py
│
└── data/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/niroop-kanchan/multi-agent-enterprise-intelligence.git
cd multi-agent-enterprise-intelligence
```

### Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Ollama Model

```bash
ollama pull llama3
```

### Run Setup Verification

```bash
python test_setup.py
```

### Launch Application

```bash
streamlit run app.py
```

---

## Skills Demonstrated

* Multi-Agent AI Systems
* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Local LLM Deployment
* OCR Pipelines
* Enterprise AI Architecture
* Streamlit Application Development
* Semantic Search
* Python Software Engineering

---

## Future Improvements

* CrewAI Agent Orchestration
* Vision Models (Llama 3.2 Vision)
* Audio Transcription
* Marketing Content Generation
* Multi-Modal AI Workflows
* Enterprise Dashboard Analytics

---

## Author

Niroop Kanchan

Engineering Student | AI Enthusiast | Building Enterprise AI Systems
