"""
agents/extraction_agent.py
---------------------------
Agent 1 – Document Extraction Agent
Reads PDFs, images (OCR), and plain-text files and returns clean text.
"""
import io
import pytesseract
from PIL import Image
from pypdf import PdfReader
from pathlib import Path


class ExtractionAgent:
    """Extract raw text from PDF, image, or text files."""

    def run(self, file_path: str) -> dict:
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            text = self._extract_pdf(path)
            source_type = "PDF"
        elif suffix in {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}:
            text = self._extract_image(path)
            source_type = "Image (OCR)"
        elif suffix in {".txt", ".md", ".csv"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            source_type = "Text"
        else:
            return {
                "success": False,
                "error": f"Unsupported file type: {suffix}",
                "text": "",
                "source_type": "Unknown",
                "filename": path.name,
            }

        text = self._clean(text)
        return {
            "success": True,
            "text": text,
            "source_type": source_type,
            "filename": path.name,
            "char_count": len(text),
            "word_count": len(text.split()),
        }

    # ------------------------------------------------------------------ #
    @staticmethod
    def _extract_pdf(path: Path) -> str:
        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                pages.append(t)
        return "\n\n".join(pages)

    @staticmethod
    def _extract_image(path: Path) -> str:
        img = Image.open(str(path))
        return pytesseract.image_to_string(img)

    @staticmethod
    def _clean(text: str) -> str:
        import re
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        return text.strip()
