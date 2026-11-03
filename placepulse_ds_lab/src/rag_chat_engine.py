"""
PlacePulse AI: RAG & Web Search Hybrid Chat Engine
Module: src/rag_chat_engine.py
Author: PlacePulse AI Team
License: Approved Production Blueprint - v1.0.0

Workflow:
Student query -> Search Knowledge Base (CSV)
  |-- Match >= threshold -> Grounded Knowledge Base response (label: "Knowledge base")
  +-- Match < threshold  -> Live Web Search via DuckDuckGo -> Grounded Web response (label: "Web" + links)
"""

import os
import re
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RAGChatEngine:
    def __init__(self, qa_csv_path: Optional[str] = None, similarity_threshold: float = 0.22):
        self.similarity_threshold = similarity_threshold
        if qa_csv_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            qa_csv_path = os.path.join(base_dir, "data", "raw", "technical_interview_qa.csv")
        
        self.qa_csv_path = qa_csv_path
        self.df_qa = pd.DataFrame()
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, stop_words="english")
        self.tfidf_matrix = None
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Loads technical_interview_qa.csv and indexes it using sublinear TF-IDF."""
        if os.path.exists(self.qa_csv_path):
            try:
                self.df_qa = pd.read_csv(self.qa_csv_path)
                corpus = (
                    self.df_qa["question"].fillna("") + " " +
                    self.df_qa["answer_summary"].fillna("") + " " +
                    self.df_qa.get("category", "").fillna("") + " " +
                    self.df_qa.get("role", "").fillna("")
                ).tolist()
                if corpus:
                    self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
            except Exception as e:
                print(f"Notice: Failed to index knowledge base ({e})")
        else:
            print(f"Notice: Knowledge base CSV not found at {self.qa_csv_path}")

    def search_knowledge_base(self, query: str) -> Tuple[Optional[Dict[str, Any]], float]:
        """
        Computes cosine similarity between student query and knowledge base corpus.
        Returns (best_match_dict, similarity_score).
        """
        if self.tfidf_matrix is None or self.df_qa.empty:
            return None, 0.0

        clean_query = query.strip()
        query_vec = self.vectorizer.transform([clean_query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        if best_score >= self.similarity_threshold:
            row = self.df_qa.iloc[best_idx].to_dict()
            return row, round(best_score, 4)
        
        return None, round(best_score, 4)

    def search_web(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """Searches the live web for tech placement & interview questions using ddgs."""
        results_list: List[Dict[str, str]] = []
        try:
            from ddgs import DDGS
            search_query = f"{query} technical placement interview"
            raw_results = list(DDGS().text(search_query, max_results=max_results))
            for item in raw_results:
                results_list.append({
                    "title": item.get("title", "Web Resource"),
                    "url": item.get("href", item.get("link", "#")),
                    "snippet": item.get("body", item.get("snippet", ""))
                })
        except Exception as e:
            # Resilient fallback query without appended keywords
            try:
                from ddgs import DDGS
                raw_results = list(DDGS().text(query, max_results=max_results))
                for item in raw_results:
                    results_list.append({
                        "title": item.get("title", "Web Resource"),
                        "url": item.get("href", item.get("link", "#")),
                        "snippet": item.get("body", item.get("snippet", ""))
                    })
            except Exception as e2:
                print(f"Notice: Web search failed ({e2})")

        return results_list

    def _call_gemini_llm(self, prompt: str, api_key: Optional[str] = None) -> Optional[str]:
        """Invokes Gemini 2.5 Flash if an API key is provided."""
        effective_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not effective_key:
            return None

        try:
            from google import genai
            client = genai.Client(api_key=effective_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            if response and hasattr(response, "text") and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Notice: Gemini LLM call skipped ({e})")
        return None

    def synthesize_answer(
        self,
        query: str,
        source: str,
        kb_match: Optional[Dict[str, Any]] = None,
        web_results: Optional[List[Dict[str, str]]] = None,
        api_key: Optional[str] = None
    ) -> str:
        """
        Synthesizes student-friendly explanation either via Gemini LLM or
        built-in structured synthesis.
        """
        if source == "Knowledge base" and kb_match:
            # Build prompt for LLM or structured synthesis
            prompt = (
                f"You are PlacePulse AI, an expert engineering campus placement mentor. "
                f"Answer the student's question based strictly on this verified technical interview knowledge base entry:\n"
                f"Question: {kb_match.get('question')}\n"
                f"Role: {kb_match.get('role')} | Category: {kb_match.get('category')} | Difficulty: {kb_match.get('difficulty')}\n"
                f"Official Answer Summary: {kb_match.get('answer_summary')}\n\n"
                f"Student Query: {query}\n\n"
                f"Instructions: Provide a clear, thorough, and highly educational explanation suitable for a technical interview round. "
                f"Include key definitions, code/architecture concepts if relevant, and practical placement tips."
            )
            llm_reply = self._call_gemini_llm(prompt, api_key)
            if llm_reply:
                return llm_reply

            # Fallback high quality synthesis
            return (
                f"### 🎯 Verified Technical Interview Answer\n\n"
                f"**Matched Topic:** {kb_match.get('question')}\n"
                f"**Domain:** `{kb_match.get('role')}` | **Category:** `{kb_match.get('category')}` | **Difficulty:** `{kb_match.get('difficulty')}`\n\n"
                f"#### Core Technical Explanation:\n"
                f"{kb_match.get('answer_summary')}\n\n"
                f"💡 **Placement Interview Tip:** In engineering technical rounds, always define the theoretical concept first, followed by a concrete real-world use case or code architecture example."
            )

        else:
            # Web Search Synthesis
            web_context = ""
            if web_results:
                for idx, r in enumerate(web_results, 1):
                    web_context += f"[{idx}] {r['title']}: {r['snippet']} (Source: {r['url']})\n"

            prompt = (
                f"You are PlacePulse AI, an expert engineering campus placement mentor. "
                f"The student asked a question not found in the local database. Here are live web search results:\n"
                f"{web_context}\n\n"
                f"Student Query: {query}\n\n"
                f"Instructions: Synthesize a concise, accurate, and structured answer answering the student's query. "
                f"Focus on practical implications for engineering campus recruitment and technical interviews."
            )
            llm_reply = self._call_gemini_llm(prompt, api_key)
            if llm_reply:
                return llm_reply

            # Fallback web synthesis
            if web_results:
                points = "\n".join([f"- **{r['title']}**: {r['snippet']}" for r in web_results])
                return (
                    f"### 🌐 Live Web Search Insights\n\n"
                    f"Here is what current technical recruitment resources and documentation state regarding your query:\n\n"
                    f"{points}\n\n"
                    f"💡 **Mentor Recommendation:** Explore the linked sources below for detailed interview patterns and practice questions."
                )
            else:
                return (
                    f"### 🌐 Web Search Summary\n\n"
                    f"No direct knowledge base entry matched your query `{query}`. We searched technical interview portals "
                    f"and recommend reviewing official documentation or foundational engineering textbooks for this concept."
                )

    def chat(self, query: str, api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Full decision pipeline:
        Query -> Knowledge Base match?
          -> Yes: Answer from CSV with label 'Knowledge base'
          -> No:  Answer from Web with label 'Web' + source links
        """
        clean_query = query.strip()
        kb_match, sim_score = self.search_knowledge_base(clean_query)

        if kb_match is not None:
            answer = self.synthesize_answer(clean_query, source="Knowledge base", kb_match=kb_match, api_key=api_key)
            return {
                "query": clean_query,
                "answer": answer,
                "source": "Knowledge base",
                "confidence": sim_score,
                "matched_question": kb_match.get("question"),
                "category": kb_match.get("category"),
                "role": kb_match.get("role"),
                "web_links": []
            }
        else:
            web_results = self.search_web(clean_query, max_results=3)
            answer = self.synthesize_answer(clean_query, source="Web", web_results=web_results, api_key=api_key)
            links = [{"title": r["title"], "url": r["url"]} for r in web_results]
            return {
                "query": clean_query,
                "answer": answer,
                "source": "Web",
                "confidence": sim_score,
                "matched_question": None,
                "category": None,
                "role": None,
                "web_links": links
            }
