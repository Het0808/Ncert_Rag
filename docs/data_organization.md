# 📂 Data Organization

This document explains how extracted content from the NCERT textbook is categorized and indexed within the **PariShiksha** system.

## 🗂️ Classification Logic
Every extracted block of text is processed and categorized into one of three primary types:

1. **CONCEPT**: Pure textbook theory, definitions, and laws (e.g., Newton's First Law).
2. **EXAMPLE**: Numerical problems and solved derivations (e.g., Calculating average speed).
3. **QUESTION**: In-text textbook exercises and end-of-chapter problems.

## 🔖 Metadata Structure
Each chunk in the retrieval index carries the following metadata to ensure accurate citation:

| Key | Description | Example |
| :--- | :--- | :--- |
| `text` | The raw text content of the chunk | "Acceleration is defined as..." |
| `page` | The physical page number in the NCERT PDF | `8` |
| `chapter` | The name of the chapter | `"Motion"` |
| `content_type` | The category identified during processing | `"concept"` |

## 🔗 Retrieval Impact
By storing the `content_type`, the system can prioritize **CONCEPT** chunks for definition-based queries and **EXAMPLE** chunks for numerical queries, ensuring the student receives the most pedagogically relevant explanation.
