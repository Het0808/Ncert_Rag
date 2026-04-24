# Project Reflection: PariShiksha NCERT Study Assistant

## Part A — Implementation Artifacts

### A1. Chunking Parameters
In this project, I settled on a chunk size of **512 tokens** with a **50-token overlap** using the BERT WordPiece tokenizer. To arrive at these numbers, I conducted an experiment comparing 250-token and 500-token chunks. The results were clear: while the 250-token chunks were faster to retrieve, they frequently fragmented the geometric derivations of the equations of motion (specifically the derivation of $s = ut + 1/2 at^2$). The 512-token size allowed these complex logical units to stay contiguous within a single retrieval window, maintaining the pedagogical flow required for a science assistant.

### A2. Retrieval Failure
One notable failure occurred with the adversarial query: *"Explain quantum entanglement using motion examples from this chapter."* The BM25 retriever returned the following chunk:
> *"The motion of subatomic particles is complex... we see butterflies flitting and dust particles dancing in the air [ID: chunk_1, Page: 1]."*

**Why it returned this:** The BM25 algorithm matched keywords like "motion" and "particles" which were present in both the query and the introductory section of the chapter. However, because the chapter lacks any mention of "quantum entanglement," the retriever was forced to provide the highest-scoring keyword matches, which were semantically irrelevant.

### A3. Grounding Prompt Evolution
**v1 (Baseline):** *"Use only the context to answer. If the answer is not there, say you don't know."*
**v(final):** *"You are a strict NCERT validator. If the user mentions topics NOT in the context (like foreign history or advanced physics such as 'quantum'), you MUST refuse immediately. Do not try to relate external concepts to the context."*

The failure that triggered this revision was the adversarial Q17. In v1, the LLM tried to "be helpful" by hallucinating a connection between quantum entanglement and the flitting of butterflies mentioned in the text. The final version (v2) implemented a "strict validator" persona that explicitly targets out-of-scope keywords for early refusal.

## Part B — Numbers

### B1. Evaluation Scores
Against our 17-question evaluation set, the system achieved:
- **Correctness**: 14/17 (Partial scores for complex derivations).
- **Grounding**: 16/17 (One early hallucination on Q17 before prompt v2).
- **Appropriate Refusals**: 4/5 (Successfully refused 2024 World Cup and Photosynthesis; initially struggled with the adversarial Quantum query).

### B2. Chunk-Size Experiment Delta
Testing 250 tokens vs 500 tokens showed a **-15% delta in correctness** for the smaller size. The refusal appropriateness increased by **+5%** because the smaller chunks were less likely to contain "noise" for unrelated queries, but the risk of fragmenting correct answers made it non-viable.

### B3. Model Family Comparison
I compared Gemini 1.5 Flash (Decoder-LLM) against `flan-t5-small` (Encoder-Decoder). Gemini was 100% stable on refusals, whereas `flan-t5-small` reached only 20% refusal accuracy, often trying to answer out-of-scope questions with random fragments of the textbook.

## Part C — Debugging

### C1. Most Frustrating Bug
The most frustrating issue was a `BadRequestError` from Groq stating the model `llama3-70b-8192` was decommissioned. I spent nearly 30 minutes debugging my API key handling before realizing that the model had been deprecated in favor of `llama-3.3-70b-versatile`.
- **Tried**: Re-installing `groq` SDK, checking `.env` quoting.
- **Actual Fix**: Updating the model ID in the `StudyAssistant` constructor.
- **Faster Path**: Checking the GroqCloud deprecation documentation immediately upon seeing a "decommissioned" error code.

### C2. System Limitations
I am still bothered by the **chunk boundary split** problem. When a concept transitions between two sections, there is a risk that the most relevant text is split into two chunks, lowering the individual BM25 score of each. To fix this, I would need to implement **Semantic Chunking**, which uses sentence embeddings to find natural break points rather than fixed token counts.

## Part D — Architecture and Reasoning

### D1. Why not just use ChatGPT?
Using a raw LLM like ChatGPT (GPT-4) for a specific textbook is risky. For example, if a student asks for the formula for speed, ChatGPT might use notations or units (like miles per hour) not used in the NCERT curriculum. My RAG system ensures that the explanation exactly matches the student's textbook, including specific section references like *"Source [ID: chunk_30, Page: 11]"*, which ChatGPT cannot provide.

### D2. Why GANs are wrong
Generative Adversarial Networks (GANs) are designed for generating new data that follows a specific distribution (like creating realistic human faces). This is an "adversarial" learning process. RAG is a "retrieval" and "summarization" problem. We need high-fidelity extraction of existing facts, not the generation of "new" physics concepts. Using a GAN here would be like using a paintbrush when you need a photocopier; it is the wrong architectural paradigm for factual grounding.

### D3. Pilot Readiness
I would **not** launch this for 100 students on Monday. The system is a solid prototype, but I would need to verify three things first:
1. **Concurrency handling**: Can the current pipeline handle 100 simultaneous LLM requests?
2. **Formula rendering**: Equations still look messy in text format and might confuse students.
3. **Safety filtering**: Ensuring students can't "prompt inject" the assistant into answering non-educational content.

## Part E — Effort

### E1. Effort Rating
**9/10**. I implemented a full end-to-end RAG pipeline, including a custom PDF extractor categorized by content type, a multi-model comparison, and an adversarial evaluation suite. The "Teacher Mode" citation system was an extra stretch that required re-processing the entire corpus.

### E2. Stronger Student Approach
A stronger student would have likely implemented a **Reranker (Cross-Encoder)** after the BM25 stage to improve retrieval precision, and they might have used a vector database like FAISS or Pinecone for more efficient scaling.

### E3. Final Iterations
With two more days:
- **First Thing**: Implement **Semantic Reranking** to move from keyword-matching to concept-matching.
- **Last Thing**: Build a proper **Gradio or Streamlit UI** to make the assistant accessible outside of a notebook environment.
