# PariShiksha NCERT Study Assistant

PariShiksha is a specialized Retrieval-Augmented Generation (RAG) system designed to help Class 9 students master the NCERT Science "Motion" chapter. Unlike general-purpose AI, PariShiksha is strictly grounded in the official textbook content, providing cited answers with specific page references.

## Core Features
- **Aesthetic Interface**: User-friendly design focuses on pedagogical clarity.
- **Strict Grounding**: Uses a two-stage prompt validation to prevent hallucinations and strictly follow NCERT material.
- **Teacher Mode**: Answers include specific citations (e.g., `[ID: chunk_14, Page: 8]`) for student verification.
- **Advanced Retrieval**: Utilizes BM25 indexing with specialized tokenization for scientific terminology.

## Getting Started

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key ([Get it here](https://aistudio.google.com/app/apikey))

### 2. Setup
```bash
git clone <repo-url>
cd ncert_rag
python -m venv venv
# Windows
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
# Required for LLM Generation
GEMINI_API_KEY=your_gemini_api_key_here

# Required for legacy features in brain.py (Optional)
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Data Preparation
The system expects the NCERT Motion chapter at `data/motion.pdf`. Due to copyright guidelines, the PDF itself is not committed to this repository. Please download `iesc104.pdf` from the [NCERT Textbook Portal](https://ncert.nic.in/textbook.php) and place it in the `data/` folder.

### 5. Running the Assistant
You can interact with the system through the provided Jupyter notebook or run the `brain.py` script for a quick test:
```bash
python brain.py
```

## System Evaluation
The system has been rigorously tested against a 17-question evaluation set covering factoids, paraphrased queries, and adversarial out-of-scope prompts. Our final results show high grounding accuracy with mandatory refusal for non-textbook topics. See `evaluation_results.md` for details.
