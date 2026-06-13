"""
agents/summary_agent.py
------------------------
Agent 3 – Summary Agent
Creates concise summaries and executive summaries from extracted text.
"""
from core.llm import get_llm
from langchain_core.messages import HumanMessage

SUMMARY_PROMPT = """\
You are a professional business writer specialising in executive communications.

Read the document below and produce:

## EXECUTIVE SUMMARY (3-4 sentences)
A high-level summary suitable for a C-suite audience.

## DETAILED SUMMARY (1-2 paragraphs)
A more thorough summary covering main points.

## KEY TAKEAWAYS
Bullet list of 5-7 actionable or important takeaways.

## RECOMMENDATIONS
2-4 concrete recommendations based on the document content.

---
DOCUMENT TEXT:
{text}
"""


class SummaryAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.3)

    def run(self, extracted_text: str) -> dict:
        truncated = extracted_text[:6000]
        prompt = SUMMARY_PROMPT.format(text=truncated)
        response = self.llm.invoke([HumanMessage(content=prompt)])
        summary = response.content if hasattr(response, "content") else str(response)
        return {"success": True, "summary": summary}
