# File: app/generator.py
"""LLM chain wrapper using modern langchain packages."""

from __future__ import annotations
from typing import Dict

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .config import settings
from .prompts import LESSON_PROMPT
from .vectorstore import get_vectorstore

class LessonPlanGenerator:
    """High-level façade for generating lesson plans via RAG."""

    def __init__(self):
        self.vs = get_vectorstore()

        self.llm = OllamaLLM(
             model=settings.LLM_MODEL,
             base_url=settings.OLLAMA_BASE_URL,
             temperature=0.8,
        )

        # 1️⃣  Prompt + LLM → combine-docs runnable
        combine_docs_chain = create_stuff_documents_chain(
            self.llm,
            LESSON_PROMPT,
        )

        # 2️⃣  Retriever + combine-docs → Retrieval chain
        self.chain = create_retrieval_chain(
            self.vs.as_retriever(search_kwargs={"k": 6}),
            combine_docs_chain,
        )

    def __call__(self, query_params: Dict) -> str:
        """Generate a lesson plan based on query parameters."""
        temp = query_params.pop("temperature", 0.2)
        # Update the shared LLM’s sampling temperature for this call
        self.llm.temperature = temp

        q = query_params.get("course_title", "") or "lesson"
        return self.chain.invoke({"input": q, **query_params})["answer"]

