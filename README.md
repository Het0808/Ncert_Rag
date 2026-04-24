# PariShiksha: Antigravity-Powered NCERT Study Assistant

**PariShiksha is a high-fidelity Retrieval-Augmented Generation (RAG) system that transforms static NCERT textbooks into interactive, cited, and strictly grounded learning experiences.**

---

## Why PariShiksha?

In the age of general-purpose LLMs, students often face two major hurdles: hallucinations and the use of non-curriculum terminology. PariShiksha solves this by anchoring every response in the official NCERT corpus.

- **Strict Pedagogical Grounding**: Unlike raw AI, PariShiksha refuses to answer from outside knowledge, ensuring students stay aligned with their syllabus.
- **Teacher-Grade Citations**: Every factual claim is backed by a specific chunk ID and page number from the textbook.
- **Scientific Precision**: Uses specialized tokenization (BERT WordPiece) to handle complex scientific terms like *specific-heat-capacity* without semantic loss.
- **Aesthetic Clarity**: Designed to be welcoming for students while maintaining the rigor of a scientific reference tool.

---

## Quick Start (Under 5 Minutes)

### 1. Initialize the Environment
```bash
git clone https://github.com/Het0808/Ncert_Rag
cd Ncert_Rag
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Your API Key
Create a `.env` file in the root:
```env
GEMINI_API_KEY=your_google_ai_studio_key
```

### 3. Run a Retrieval Test
```python
from brain import StudyAssistant
assistant = StudyAssistant()
for response in assistant.ask_with_context("What is motion?", "Motion is change in position."):
    print(response, end="")
```

---

## Core Features

### 📡 Multi-Stage Retrieval
PariShiksha uses **BM25Okapi** indexing to find the most relevant conceptual paragraphs, worked examples, and exercises. This ensures that the most "pedagogically dense" content is prioritized.

### 📝 Verified "Teacher Mode"
The assistant doesn't just answer; it justifies. By including scholarly citations, it teaches students how to find information within their own books.
```text
"Acceleration is the rate of change of velocity [ID: chunk_22, Page: 8]."
```

### 🛡️ Adversarial Grounding
Equipped with a strict "Refusal Instruction" Layer, the system can detect and reject out-of-scope queries (e.g., history, unrelated sciences) with a mandatory refusal message, maintaining a focused study environment.

---

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google AI Studio API Key | Required |
| `CHUNK_SIZE` | Context tokens per chunk | 512 |
| `CHUNK_OVERLAP` | Token overlap for continuity | 50 |
| `MODEL_NAME` | The LLM engine used for generation | `gemini-1.5-flash` |

---

## Installation & Requirements

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.10+
- **Memory**: 4GB+ (for local tokenizer handling)

### Package Managers
- **Pip**: `pip install -r requirements.txt`
- **Conda**: `conda env create -f environment.yml` (Coming Soon)

---

## Usage Examples

### Conceptual Deep-Dive
Retrieve the exact paragraph explaining the difference between distance and displacement.
```python
# See notebook.ipynb Cell 11 for retrieval implementation
results = retrieve("Difference between distance and displacement")
```

### Evaluation Mode
Run a rigorous 3-axis evaluation (Correctness, Grounding, Refusal) using the integrated `evaluation_set.csv`.

---

## Contributing
We welcome contributions from the educational and AI communities!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Dependencies
- `PyMuPDF` (Text extraction)
- `rank_bm25` (Retrieval indexing)
- `transformers` & `torch` (Tokenization)
- `google-generativeai` (LLM Generation)
- `python-dotenv` (Key management)

---

## License & Acknowledgments
Distributed under the MIT License. See `LICENSE` for more information.

*Special thanks to the NCERT for providing high-quality educational resources for Indian students.*

---
**PariShiksha** — *Education, Grounded in Truth.*
