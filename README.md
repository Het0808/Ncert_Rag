# PariShiksha: NCERT Study Assistant (Powered by Groq)

**PariShiksha is a high-performance Retrieval-Augmented Generation (RAG) system that uses Groq's LPU™ Inference Engine to provide ultra-fast, strictly-grounded answers from the NCERT Class 9 Science textbook.**

---

## Why PariShiksha?

PariShiksha is designed for pedagogical safety, ensuring that Class 9 students receive answers that are strictly aligned with their curriculum while avoiding the hallucinations common in general AI.

- **Extreme Performance**: Powered by Groq for near-instantaneous student Q&A.
- **Academic Grounding**: Every response is anchored in the "Motion" chapter of the NCERT Science textbook.
- **Citation Metadata**: In "Teacher Mode," answers include specific chunk references (e.g., `[ID: chunk_14, Page: 8]`) directly from the source.
- **Robust Evaluation**: Evaluated against a 17-question rigorous test set, including adversarial out-of-scope queries to ensure contextual accuracy.

---

## Quick Start (3 Minutes)

### 1. Initialize the Repository
```bash
git clone https://github.com/Het0808/Ncert_Rag
cd Ncert_Rag
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Your API Key
Create a `.env` file in the root directory:
```env
# Required for brain.py and Retrieval Tests
GROQ_API_KEY=gsk_your_groq_key_here
```

### 3. Run the Assistant
```bash
python brain.py
```

---

## Core Features

### 📡 Systematic Retrieval
Uses the `rank_bm25` algorithm combined with a **BERT WordPiece** tokenizer to find technical concepts like *velocity* and *displacement* even when phrased differently by students.

### 🛡️ Adversarial Logic
Unlike standard chat bots, PariShiksha is instructed to refuse questions not found in the chapter (e.g., history or unrelated sciences) with a mandatory refusal message: *"I cannot answer this from the provided chapter content."*

### 📏 Flexible Chunking
Implements a 512-token chunking strategy with a 50-token overlap, ensuring that large conceptual blocks like "Equations of Motion" remain contiguous.

---

## Project Structure

- **`notebook.ipynb`**: End-to-end development pipeline (Processing -> Retrieval -> Generation).
- **`brain.py`**: Production-ready implementation using the Groq SDK.
- **`evaluation_results.md`**: Scoring of the system against 3 axes: Correctness, Grounding, and Refusal.
- **`reflection.md`**: Technical report on architecture decisions and failure analysis.

---

## Installation & Requirements

### System Requirements
- **OS**: Windows (tested), macOS, or Linux
- **Python**: 3.10+
- **Key**: A valid Groq API Key from [console.groq.com](https://console.groq.com/).

### Installation
```bash
pip install -r requirements.txt
```

---

## Contributing
Community participation is welcome! Please follow the contribution guidelines in the repository for bug reports or feature requests.

---

## License
Distributed under the MIT License.

---
**PariShiksha** — *Scientific Study, Reimagined through RAG.*
