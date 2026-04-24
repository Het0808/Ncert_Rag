# Systematic Evaluation Guide for ML & RAG Systems

Evaluating a machine learning project—especially a **Retrieval-Augmented Generation (RAG)** system like yours—requires looking beyond simple accuracy. You need to test the **data retrieval**, the **response generation**, and the **system integrity**.

---

## 1. Pre-testing Preparation
Before you write a single line of test code, you need a "Gold Standard" to measure against.

### A. The Evaluation Set (Ground Truth)
You must create a representative dataset. For your NCERT Study Assistant, this is your `evaluation_set.csv`.
- **Diverse Queries**: Include "easy" factual questions, "complex" conceptual questions, and "adversarial" out-of-scope questions.
- **Expected Responses**: For RAG, you need both the **Expected Answer** and the **Expected Sources** (e.g., Page 5).

### B. Metrics Selection
- **Classification Metrics**: Accuracy, Precision, Recall (Best for the "Refusal" logic).
- **RAG-Specific Metrics**:
    - **Faithfulness**: Does the answer come *only* from the context?
    - **Relevance**: Did we retrieve the *right* chunks for the question?

---

## 2. Accuracy Testing Techniques
"Accuracy" means different things depending on the layer of the model.

### A. Component-Level Accuracy (Unit Testing)
- **Retrieval Accuracy**: Use **Top-k Recall**. If the answer is on page 10, did your search engine (BM25) return page 10 in the top 3 results?
- **Classification Accuracy**: As we implemented in `test_model.py`, check if the model correctly labels a question as "out of scope."

### B. LLM Output Evaluation
Since LLM output is free-text, simple string matching fails. Use:
- **LLM-as-a-Judge**: Use a stronger model (like GPT-4 or Gemini 1.5 Pro) to grade your current model's answers on a scale of 1-5.
- **Semantic Similarity**: Use embedding vectors to see how close the answer is to the ground truth.

---

## 3. Full Project Testing (End-to-End)
A model is only as good as the pipeline feeding it.

- **Data Pipeline Testing**: If you add a new PDF, does the `prepare_corpus` function break on weird characters or table headers?
- **Integration Points**: Test the transition from `retrieve()` to `answer()`. If `retrieve()` returns empty chunks, does `answer()` handle it gracefully?
- **Preprocessing Robustness**: Test with typos (e.g., "What is accelaration?") to see if your tokenizer/BM25 can still find the right data.

---

## 4. Validation Approach
To ensure your model doesn't just "memorize" your test questions (overfitting):

- **Train/Test/Validation Splits**:
    - **Train**: Data used to build your search index.
    - **Validation**: Samples used to tune your "k" (number of retrieved chunks) or prompt wording.
    - **Test**: The final set you only use *once* to get your true accuracy.
- **Cross-Validation**: For RAG, this might mean testing across different chapters of the textbook to ensure the prompt works generally, not just for the "Motion" chapter.

---

## 5. The Testing Workflow
Follow this sequence to save time:

1.  **Smoke Test**: Does the code run without crashing?
2.  **Retrieval Test**: Measure Top-k Recall. If retrieval is bad, the RAG system will always fail.
3.  **Refusal Test**: Check if the model incorrectly answers "Who is Napoleon?" (False Positives).
4.  **Generation Test**: Use your evaluation set to check factual correctness.
5.  **Performance Test**: Measure latency (how many seconds per answer).

---

## 6. Interpreting Results
- **High Accuracy, Low Satisfaction**: You might be testing on questions that are too easy. Add harder, paraphrased questions.
- **High Refusal Rate**: Your prompt may be "too strict." Try loosening the instructions in `brain.py`.
- **Good Retrieval but Wrong Answer**: Your prompt or the LLM's reasoning is the bottleneck, not the data.

---

## 7. Common Pitfalls
*   **Data Leakage**: Testing on questions that were accidentally included in your "system prompt" or examples.
*   **The LLM Hallucination Trap**: Just because an answer looks professional doesn't mean it's accurate. **Always** verify against the source page.
*   **Over-Optimization**: Changing your prompt so it handles one specific question perfectly, but breaks five others. Always re-run the *full* `test_model.py` after a prompt change.

---

### Recommended Toolset
- **Pandas/Scikit-learn**: For data handling and metrics (already installed).
- **RAGAS**: A specialized framework for evaluating RAG systems.
- **Gradio/Streamlit**: For manual "vibe checks" during development.
