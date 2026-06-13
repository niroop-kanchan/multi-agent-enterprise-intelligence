"""
test_setup.py  –  Run this BEFORE launching the app to verify everything works.
Usage: python test_setup.py
"""
import sys

def check(label, fn):
    try:
        fn()
        print(f"  ✅  {label}")
        return True
    except Exception as e:
        print(f"  ❌  {label}  →  {e}")
        return False

print("\n🔍  MAEIS – Setup Verification\n" + "=" * 40)

# Python version
print(f"\n[1] Python  {sys.version.split()[0]}")
if sys.version_info < (3, 10):
    print("  ⚠️  Python 3.10+ recommended")
else:
    print("  ✅  Python version OK")

# Imports
print("\n[2] Package imports")
check("streamlit",            lambda: __import__("streamlit"))
check("crewai",               lambda: __import__("crewai"))
check("langchain_ollama",     lambda: __import__("langchain_ollama"))
check("chromadb",             lambda: __import__("chromadb"))
check("pypdf",                lambda: __import__("pypdf"))
check("pytesseract",          lambda: __import__("pytesseract"))
check("Pillow (PIL)",         lambda: __import__("PIL"))
check("sentence_transformers",lambda: __import__("sentence_transformers"))
check("fpdf2 (fpdf)",         lambda: __import__("fpdf"))
check("ollama SDK",           lambda: __import__("ollama"))

# Tesseract binary
print("\n[3] Tesseract OCR binary")
import shutil
if shutil.which("tesseract"):
    print("  ✅  tesseract found in PATH")
else:
    print("  ❌  tesseract NOT found – install Tesseract and add to PATH")

# Ollama
print("\n[4] Ollama server")
try:
    import ollama
    models = ollama.list()
    names = [m.model for m in models.models]
    print(f"  ✅  Ollama running  |  models: {names or 'none pulled yet'}")
    if not any("llama3" in n or "gemma" in n for n in names):
        print("  ⚠️  No llama3/gemma found – run: ollama pull llama3")
except Exception as e:
    print(f"  ❌  Ollama not running  →  {e}")
    print("       Start it with: ollama serve")

# Directories
print("\n[5] Data directories")
import os
for d in ["data/uploads", "data/reports", "data/chroma_db"]:
    os.makedirs(d, exist_ok=True)
    print(f"  ✅  {d}")

print("\n" + "=" * 40)
print("Done! If all green → run:  streamlit run app.py\n")
