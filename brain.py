import os
import re
import fitz
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from rank_bm25 import BM25Okapi
from transformers import AutoTokenizer

load_dotenv()

class StudyAssistant:
    def __init__(self, pdf_path="data/motion.pdf", model="llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        
        self.client = Groq(api_key=self.api_key)
        self.model = model
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        
        # RAG Parameters
        self.max_tokens = 450 # Stay under BERT's 512 limit
        self.overlap = 50
        self.chunks = []
        
        if os.path.exists(pdf_path):
            self._prepare_corpus(pdf_path)
            self._build_index()
        else:
            print(f"Error: PDF not found at {pdf_path}. Please check the path.")
            self.bm25 = None

    def _prepare_corpus(self, pdf_path):
        """
        Improved chunking strategy: Uses a sliding window with token-count awareness.
        This prevents the 512-token limit warning and ensures no context is truncated.
        """
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            text = page.get_text("text")
            # Clean up text (remove excessive whitespace)
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Tokenize the entire page text
            tokens = self.tokenizer.encode(text, add_special_tokens=False)
            
            # Create overlapping chunks
            for j in range(0, len(tokens), self.max_tokens - self.overlap):
                chunk_tokens = tokens[j : j + self.max_tokens]
                chunk_text = self.tokenizer.decode(chunk_tokens)
                
                self.chunks.append({
                    "text": chunk_text,
                    "page": i + 1,
                    "chapter": "Motion"
                })

    def _build_index(self):
        """
        Tokenizes the chunks for BM25 indexing. 
        Since we ensured chunks < 512 tokens, this won't trigger truncation warnings.
        """
        tokenized_corpus = [self.tokenizer.tokenize(c['text']) for c in self.chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def retrieve(self, query, k=3):
        """Retrieves the top-k most relevant chunks using BM25."""
        if not self.chunks or self.bm25 is None:
            return []
            
        tokenized_query = self.tokenizer.tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        # Select top-k indices based on BM25 scores
        top_n_indices = np.argsort(scores)[::-1][:k]
        return [self.chunks[i] for i in top_n_indices]

    def answer(self, question):
        results = self.retrieve(question)
        
        # Build context with clear XML tags for the LLM
        context_parts = []
        for i, r in enumerate(results):
            context_parts.append(f"<document index='{i}' page='{r['page']}'>\n{r['text']}\n</document>")
        context = "\n".join(context_parts)
        
        # FINAL STRICT PROMPT:
        # Designed to hit 85-90% accuracy by eliminating hallucinations on out-of-scope topics.
        system_prompt = (
            "You are a strict NCERT Science Validator.\n"
            "Answering out-of-scope questions is a CRITICAL FAILURE.\n\n"
            "TASK: Answer the question using ONLY the provided <context>.\n\n"
            "EVALUATION PROCESS:\n"
            "1. Read the question.\n"
            "2. Search the <context> for the specific topic.\n"
            "3. If the topic (e.g., Photosynthesis, Napoleon, Cell Division) is NOT the main subject of any <document> block, you MUST respond with the refusal message.\n"
            "4. NEVER use outside knowledge to supplement the answer.\n"
            "5. If you answer, you MUST cite the [Page X].\n\n"
            "REFUSAL MESSAGE: 'I cannot answer this from the provided chapter content.'\n\n"
            "Example of Failure: Answering 'What is photosynthesis?' because the word 'oxygen' appeared in a motion context. DO NOT DO THIS. Refuse if 'Photosynthesis' is not explicitly explained."
        )
        
        user_content = f"<context>\n{context}\n</context>\n\nQUESTION: {question}"

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0, # Essential for predictable grounding
                stream=True
            )
            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            yield f"[Error Calling API: {str(e)}]"

if __name__ == "__main__":
    assistant = StudyAssistant()
    print("Test Query: What is acceleration?")
    for text in assistant.answer("What is acceleration?"):
        print(text, end="", flush=True)
