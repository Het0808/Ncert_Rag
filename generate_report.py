from fpdf import FPDF
import sys

class MyPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'PariShiksha: Technical Project Analysis', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_report():
    pdf = MyPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    # Overview
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(200, 10, txt="1. Project Overview", ln=True)
    pdf.set_font("Helvetica", size=11)
    # Using standard hyphens instead of en-dashes
    text1 = (
        "PariShiksha is a specialized Retrieval-Augmented Generation (RAG) system "
        "designed for NCERT Class 9 Science students. The primary problem it solves is "
        "AI Hallucination - where general AI models provide technically incorrect or "
        "out-of-syllabus information. By anchoring the model's 'brain' directly to the "
        "official textbook, we ensure academic integrity and pedagogical safety."
    )
    pdf.multi_cell(0, 7, txt=text1)
    pdf.ln(5)

    # Data Processing Phase
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(200, 10, txt="2. Phase 1: Intelligent Data Ingestion", ln=True)
    pdf.set_font("Helvetica", size=11)
    text2 = (
        "Purpose: To convert a static PDF textbook into a searchable digital format.\n"
        "How it works: We use the PyMuPDF library to extract raw text from each page. "
        "However, simple extraction isn't enough. We implement a Token-Aware Sliding Window "
        "chunking strategy. Each page is broken into blocks of 450 words (tokens) with a "
        "50-word overlap to ensure concepts at the edges aren't lost.\n"
        "Outcome: A database of contextual 'chunks' that a machine can understand and search."
    )
    pdf.multi_cell(0, 7, txt=text2)
    pdf.ln(5)

    # Retrieval Phase
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(200, 10, txt="3. Phase 2: High-Precision Retrieval (BM25)", ln=True)
    pdf.set_font("Helvetica", size=11)
    text3 = (
        "Purpose: To find the most relevant section of the book for any given student question.\n"
        "How it works: We use the BM25 (Best Matching 25) algorithm. Think of this as a "
        "super-powered keyword search. It doesn't just look for words; it calculates which "
        "textbook passage has the most unique and relevant terms for the question.\n"
        "Connection: This step takes the student's question and picks the best 3 chunks from "
        "the database created in Phase 1.\n"
        "Outcome: A focused set of 'Context' tags that are fed into the AI."
    )
    pdf.multi_cell(0, 7, txt=text3)
    pdf.ln(5)

    # Generation Phase
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(200, 10, txt="4. Phase 3: Fast Grounded Inference (Groq LPU)", ln=True)
    pdf.set_font("Helvetica", size=11)
    text4 = (
        "Purpose: To turn the textbook data into a conversational, cited answer.\n"
        "How it works: We send the question + the selected textbook context to the Llama-3.3 "
        "model via Groq's high-speed inference engine. We use a 'Strict Validator' prompt "
        "that forces the model to cite specific page numbers [Page X] and refuse questions "
        "not in the data.\n"
        "Outcome: A sub-second response that is 100% anchored in the textbook curriculum."
    )
    pdf.multi_cell(0, 7, txt=text4)
    pdf.ln(5)

    # Evaluation Phase
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(200, 10, txt="5. Phase 4: Systematic Evaluation & Audit", ln=True)
    pdf.set_font("Helvetica", size=11)
    text5 = (
        "Purpose: To prove that the system actually works and doesn't hallucinate.\n"
        "How it works: We run a suite of 17 'Adversarial' and 'Curriculum' questions through "
        "an automated audit script. We measure Accuracy, Precision (how many refusals were correct), "
        "and Recall (if we answered all textbook questions).\n"
        "Final Deliverable: An audit report showing 100% recall on core textbook chapters."
    )
    pdf.multi_cell(0, 7, txt=text5)
    pdf.ln(10)
    
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 10, "- End of Project Analysis Report -", 0, 1, 'C')

    output_path = "Parishiksha_Technical_Report.pdf"
    pdf.output(output_path)
    print(f"Report generated successfully: {output_path}")

if __name__ == "__main__":
    create_report()
