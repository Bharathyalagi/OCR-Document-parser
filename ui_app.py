import streamlit as st
from PIL import Image
import pytesseract
from llm_parser import parse_text_with_llm
import json

# Set Tesseract path (only if required for Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("Document Parser UI")

# Upload document
uploaded_file = st.file_uploader("Upload your document (jpg, png)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Document", use_column_width=True)

    # Extract text using OCR
    text = pytesseract.image_to_string(image)
    st.subheader("OCR Extracted Text")
    st.text_area("Text Output", text, height=200)

    # Get structured output
    structured_output = parse_text_with_llm(text)
    parsed_data = json.loads(structured_output)  # convert JSON string to dictionary

    # Input field for key search
    st.subheader("Search Specific Field")
    key_to_search = st.text_input("Enter field name (Example: Name, Phone, Email, LinkedIn, GitHub, Date of Birth, Address, Skill)")

    if key_to_search:
        key_to_search_lower = key_to_search.strip().lower()

        # Search matching key
        result = None
        for k, v in parsed_data.items():
            if key_to_search_lower == k.lower():
                result = v
                break

        if result:
            st.success(f"**{key_to_search}**: {result}")
        else:
            st.error(f"No field found for: {key_to_search}")

    # Show full JSON option
    if st.checkbox("Show Full JSON Output"):
        st.json(parsed_data)
