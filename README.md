# PariShiksha NCERT Study Assistant

A retrieval-augmented QA system for NCERT Class 9 Science, designed to help students interact with their textbooks using AI.

## Project Description
PariShiksha uses Retrieval-Augmented Generation (RAG) to provide accurate answers from the NCERT Class 9 Science textbook. It processes PDF chapters, indexes the content using BM25 and vector embeddings, and uses Gemini AI to answer queries with context.

## Setup Instructions

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone the Repository
```bash
git clone <your-repo-url>
cd ncert_rag
```

### 3. Set up Virtual Environment
```bash
python -m venv venv
# Activate on Windows:
.\venv\Scripts\activate
# Activate on macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure API Key
1. Create a `.env` file in the root directory.
2. Add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

### 6. Download NCERT Chapters
Download the PDF chapters from the official link below and place them in a `data/` folder (do not commit them).

**NCERT Source:** [Class 9 Science (Classroom)](https://ncert.nic.in/textbook.php?iesc1=0-11)

---
*Note: PDFs are for educational use only according to NCERT guidelines. Do not commit PDF files to this repository.*
