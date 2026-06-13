"""
agents/research_agent.py
-------------------------
Agent 2 – Research Agent
Analyses extracted text: finds key topics, entities, keywords, and insights.
"""
from core.llm import get_llm
from langchain_core.messages import HumanMessage

RESEARCH_PROMPT = """\
You are an expert enterprise research analyst.

Analyse the document text below and produce a structured research report.

Return ONLY the following sections (use these exact headings):

## KEY TOPICS
List the 5-10 main topics covered.

## NAMED ENTITIES
List people, organisations, locations, dates, and numbers mentioned.

## KEYWORDS
List 10-15 important keywords or phrases.

## KEY INSIGHTS
List 5-8 important insights or findings.

## SENTIMENT
Overall tone of the document (positive / neutral / negative) with a one-line reason.

---
DOCUMENT TEXT:
{text}
"""


class ResearchAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.2)

    def run(self, extracted_text: str) -> dict:
        truncated = extracted_text[:6000]  # stay within context window
        prompt = RESEARCH_PROMPT.format(text=truncated)
        response = self.llm.invoke([HumanMessage(content=prompt)])
        analysis = response.content if hasattr(response, "content") else str(response)
        return {
            "success": True,
            "analysis": analysis,
            "input_words": len(extracted_text.split()),
        }
