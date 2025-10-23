# OCR Document Parser (Tesseract + Streamlit)

Small OCR system to parse PAN cards, resumes and handwritten docs.
- Backend: Tesseract (via pytesseract)
- Parser: `llm_parser.py` (regex-based extraction + simple heuristics)
- UI: Streamlit app `ui_app.py`
- Batch runner: `main.py` (processes `sample_docs/` and writes JSON to `outputs/`)

## Quick Start

1. Install Python 3.8+ and Tesseract OCR
2. Clone or download this repo
3. Install Python deps:
   ```bash
   pip install -r requirements.txt
   ```
4. Run CLI Batch
   ```bash
   python main.py
   ```
5. Run web UI
   ```bash
   streamlit run ui_app.py
   ```
