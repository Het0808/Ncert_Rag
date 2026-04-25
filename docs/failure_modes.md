# RAG Failure Modes & Mitigation Strategies

This document analyzes the specific failure points identified during the auditing of **PariShiksha v1.0** and proposes advanced mitigation strategies.

---

## 1. The "Semantic Drift" Failure
**Symptom**: The model attempts to answer questions about distant science topics (like Photosynthesis) by connecting them to irrelevant words in the textbook.

### Case Study: Photosynthesis
- **Query**: "What are the primary products of photosynthesis?"
- **Retrieved Context**: Chunks discussing "oxygen" and "gathering clouds" in the introduction of the Motion chapter.
- **Error**: The LLM identified the word "oxygen" in the context and used its internal knowledge of photosynthesis to construct a "helpful" answer, ignoring the refusal instruction.

### Mitigation: Semantic Distance Guarding
Instead of relying solely on prompt instructions, we can implement an **Embedding-Based Threshold**:
1. Calculate the cosine similarity between the query and the top-k retrieved chunks.
2. If the similarity score is below a threshold (e.g., 0.4), trigger an automatic refusal before the LLM is even called.

---

## 2. The "Equation Fragmentation" Failure
**Symptom**: The model provides a formula but fails to provide the full derivation or logical proof.

### Case Study: Second Equation of Motion
- **Query**: "Derive s = ut + 1/2 at^2"
- **Cause**: The derivation spans multiple pages in the NCERT PDF. If the pages are not contiguous in a single chunk, the logical flow is broken.

### Mitigation: Hierarchical Retrieval
Instead of flat chunking, use a **Parent-Child Retriever**:
1. Store large "Parent" chunks (full sections) alongside small "Child" chunks (paragraphs).
2. Use the "Child" chunks for retrieval, but feed the entire "Parent" context to the LLM.

---

## 3. The "Adversarial Bridging" Failure
**Symptom**: The model follows an adversarial instruction like "Explain X using concepts from the chapter."

### Case Study: Quantum Entanglement
- **Error**: The model tried to use "random motion" as a metaphor for "quantum entanglement."

### Mitigation: Negative Constraint Prompting
Implement a **Strict Refusal Classifier**:
1. Run the query through a fast classifier (like DistilBERT) trained on out-of-scope NCERT questions.
2. If the classifier flags the query as "Adversarial," the system prompt is automatically swapped with a much stricter version.

---

## Summary of Audit Findings
| Failure Type | Frequency | Status | Primary Fix |
| :--- | :--- | :--- | :--- |
| **False Negative** | Low | **Resolved** | Sliding Window Chunking |
| **False Positive** | Moderate | **Mitigated** | XML Grounding Tags |
| **Truncation** | High | **Resolved** | 450-Token Max Window |
| **Hallucination** | Low | **Stable** | Temperature 0 + Strict Roleplay |
