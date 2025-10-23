from ocr_engine import extract_text
from llm_parser import parse_text_with_llm
import os

# Process both docs
files = ["resume.png", "handwritten.png", "pan_card.jpg"]

for file in files:
    image_path = os.path.join("sample_docs", file)
    text = extract_text(image_path)
    print(f"\n===== OCR Output for {file} =====\n{text}\n")

    structured_output = parse_text_with_llm(text)
    print(f"===== Structured Output for {file} =====\n{structured_output}\n")

    # Save each output
    output_file = os.path.join("outputs", f"{file.split('.')[0]}_result.json")
    with open(output_file, "w") as f:
        f.write(structured_output)

print("\nAll outputs saved in outputs/ folder")
