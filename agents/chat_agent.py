"""
agents/chat_agent.py
---------------------
Agent 5 – Chat Agent (RAG)
Answers user questions by retrieving relevant chunks from ChromaDB
then asking the LLM to answer using only that context.
"""
from core.llm import get_llm
from core.knowledge_base import KnowledgeBase
from langchain_core.messages import HumanMessage

RAG_PROMPT = """\
You are an expert enterprise assistant. Answer the user's question using ONLY
the context passages provided below. If the answer is not in the context, say
"I could not find that information in the uploaded documents."

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:"""


class ChatAgent:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.llm = get_llm(temperature=0.4)

    def chat(self, question: str) -> dict:
        if self.kb.count() == 0:
            return {
                "answer": "No documents have been uploaded yet. Please upload and process a file first.",
                "context_chunks": [],
            }

        context_chunks = self.kb.query(question, n_results=5)
        context = "\n\n---\n\n".join(context_chunks) if context_chunks else ""

        prompt = RAG_PROMPT.format(context=context, question=question)
        response = self.llm.invoke([HumanMessage(content=prompt)])
        answer = response.content if hasattr(response, "content") else str(response)

        return {"answer": answer, "context_chunks": context_chunks}
