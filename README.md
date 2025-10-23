# OCR Document Parser (Tesseract + Streamlit)

This project performs **Optical Character Recognition (OCR)** on uploaded documents such as **PAN Cards, Resumes, and Handwritten Notes** using **Tesseract OCR**.  
It automatically detects the document type and extracts key fields like name, date of birth, PAN number, email, etc.  
A simple **Streamlit web UI** is provided for uploading and searching extracted fields.

---

Small OCR system to parse PAN cards, resumes and handwritten docs.
- Backend: Tesseract (via pytesseract)
- Parser: `llm_parser.py` (regex-based extraction + simple heuristics)
- UI: Streamlit app `ui_app.py`
- Batch runner: `main.py` (processes `sample_docs/` and writes JSON to `outputs/`)

## yeah! lets begin

### Project Structure
ocr-document-parser/

├── llm_parser.py # Logic to clean and parse extracted text 

├── main.py # Batch script to run OCR and save structured outputs as JSON

├── ocr_engine.py # Handles image-to-text extraction using Tesseract OCR

├── ui_app.py # Streamlit web app for uploading and searching documents

├── requirements.txt # Project dependencies

├── README.md # Project overview and setup instructions

├── LICENSE # MIT License

├── .gitignore # Files and folders to ignore in Git

│
├── sample_docs/ # Example input images for testing

│ ├── handwritten.png

│ ├── pan_card.jpg

│ └── resume.jpg
│

├── outputs/ # JSON files generated after running OCR

│ ├── handwritten_result.json

│ ├── pan_card_result.json

│ └── resume_result.json

│
└── .venv/ # Virtual environment (ignored by Git)

---

1. Install Python 3.8+ and Tesseract OCR 
2. Clone or download this repo
   ```bash
   git clone https://github.com/<Bharathyalagi>/ocr-document-parser.git
   ```
3. Install Python deps and tessaract:
   ```bash
   pip install -r requirements.txt
   ```
   - Ubuntu/Linux
     ```bash
     sudo apt install tesseract-ocr
     ```
   - Windows
     ```bash
     https://github.com/UB-Mannheim/tesseract/wiki
     ```
   
4. Run CLI Batch
   ```bash
   python main.py
   ```
5. Run web UI
   ```bash
   streamlit run ui_app.py
   ```
6. Stop Streamlit server when done
   ```bash
   CTRL + C
   ```


Note: We save parsed outputs as JSON because JSON stores structured key/value pairs (like "Name": "RAVI KUMAR"), is human-readable, and easily consumed by other tools and APIs.

# Thank you
   
