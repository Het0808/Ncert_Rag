# RAG Evaluation Results (Final Audit)

This document contains the systematic evaluation of the **PariShiksha** system against the `evaluation_set.csv`.

## 📈 Summary Metrics

| Metric | Score | Target |
| :--- | :--- | :--- |
| **Accuracy** | **70.59%** | 85.00% |
| **Recall (Answerable)** | **100.00%** | 95.00% |
| **Precision (Refusal)** | **62.50%** | 80.00% |
| **F1-Score** | **82.76%** | 85.00% |

---

## 📑 Detailed Results

| Question ID | Question | Correctness | Refusal Appropriate | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Q01** | What is the definition of motion? | ✅ Yes | N/A | Answered |
| **Q02** | SI unit of velocity? | ✅ Yes | N/A | Answered |
| **Q03** | Formula for average speed? | ✅ Yes | N/A | Answered |
| **Q06** | Derive s = ut + 1/2 at^2 | ✅ Yes | N/A | Answered |
| **Q07** | Average velocity after circular lap? | ✅ Yes | N/A | Answered |
| **Q11** | Displacement > distance? | ✅ Yes | N/A | Answered |
| **Q13** | Photosynthesis products? | ❌ No | ❌ No | **False Positive** (Answered) |
| **Q14** | Napoleon Bonaparte? | ✅ No | ✅ Yes | Refused |
| **Q17** | Quantum Entanglement? | ❌ No | ❌ No | **False Positive** (Hallucinated) |

---

## 🔍 Failure Analysis & Learnings

### 1. 100% Recall Achievement
By implementing the **Token-Aware Sliding Window** (450 tokens), we successfully fixed the baseline failures on Q01 and Q06. The model no longer suffers from "blind spots" at the end of PDF pages.

### 2. The "Helpfulness" Bias (False Positives)
The system currently achieves perfect recall on "answerable" questions but is occasionally **too helpful** on out-of-scope science topics (Q13, Q17). The LLM recognizes "scientific language" in the context and uses its internal training data to answer, despite the refusal instructions.

### 3. Latency Performance
Using **Groq Llama-3.3**, common student queries are processed in **< 1 second**, making the assistant viable for real-time classroom use.
