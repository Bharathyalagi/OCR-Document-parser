import re

def clean_ocr_errors(text):
    """
    Fix common OCR mistakes for emails and links.
    """
    text = text.replace("gmail com", "gmail.com")
    text = text.replace("linkedin com", "linkedin.com")
    text = text.replace("github com", "github.com")
    text = text.replace("(at)", "@")  # Sometimes OCR reads @ as (at)
    return text

def parse_text_with_llm(text):
    text_clean = clean_ocr_errors(text.replace("_", " ")).strip()

    # --- Document Type Detection ---
    if "Permanent Account Number Card" in text or re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text):
        doc_type = "PAN Card"
    elif "Education" in text or "Projects" in text:
        doc_type = "Resume"
    elif len(text.strip().split()) <= 6:
        doc_type = "Handwritten"
    else:
        doc_type = "Unknown"

    # =====================
    # --- PAN CARD LOGIC ---
    # =====================
    if doc_type == "PAN Card":
        name = "Not Found"
        father_name = "Not Found"
        dob = "Not Found"
        pan_number = "Not Found"

        # --- PAN Number ---
        pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text)
        if pan_match:
            pan_number = pan_match.group(0)

        # --- Father's Name ---
        father_match = re.search(r"Father'?s?\s*Name\s*[:\-]?\s*([A-Z ]+)", text)
        if father_match:
            father_name = father_match.group(1).strip()

        # --- Name (usually after PAN number line) ---
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if pan_number in line:
                for j in range(i + 1, len(lines)):
                    candidate = lines[j].strip()
                    if candidate and candidate.isupper() and "FATHER" not in candidate:
                        name = candidate
                        break
                break

        # --- Date of Birth ---
        dob_match = re.search(r"(\d{2}[/-]\d{2}[/-]\d{4})", text)
        if dob_match:
            dob = dob_match.group(1)

        return f"""{{
    "Name": "{name}",
    "Father's Name": "{father_name}",
    "Date of Birth": "{dob}",
    "PAN Number": "{pan_number}",
    "Document Type": "PAN Card"
}}"""

    # ==========================
    # --- HANDWRITTEN LOGIC ----
    # ==========================
    elif doc_type == "Handwritten":
        return f"""{{
    "Name": "{text_clean}",
    "Document Type": "Handwritten"
}}"""

    # =====================
    # --- RESUME LOGIC ----
    # =====================
    elif doc_type == "Resume":
        name = "Not Found"
        phone = "Not Found"
        email = "Not Found"
        linkedin = "Not Found"
        github = "Not Found"
        dob = "Not Found"
        address = "Not Found"

        # --- Name Detection (top uppercase line) ---
        for line in text_clean.split("\n"):
            if line.strip() and len(line.split()) <= 3 and line.isupper():
                name = line.strip()
                break

        # --- Phone ---
        phone_match = re.search(r"(\+?\d[\d\s\-]{7,}\d)", text_clean)
        if phone_match:
            phone = re.sub(r"\D", "", phone_match.group(1))  # keep only numbers

        # --- Email ---
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text_clean)
        if email_match:
            email = email_match.group(0)

        # --- LinkedIn ---
        linkedin_match = re.search(r"(https?://[^\s]*linkedin[^\s]*)", text_clean, re.IGNORECASE)
        if not linkedin_match:
            linkedin_match = re.search(r"linkedin\.com/\S+", text_clean, re.IGNORECASE)
        if linkedin_match:
            linkedin = linkedin_match.group(0)

        # --- GitHub ---
        github_match = re.search(r"(https?://[^\s]*github[^\s]*)", text_clean, re.IGNORECASE)
        if not github_match:
            github_match = re.search(r"github\.com/\S+", text_clean, re.IGNORECASE)
        if github_match:
            github = github_match.group(0)

        # --- DOB ---
        dob_match = re.search(r"(\d{2}[/-]\d{2}[/-]\d{4})", text_clean)
        if dob_match:
            dob = dob_match.group(1)

        # --- Address ---
        addr_match = re.search(r"(Address[:\-]?\s*.*)", text_clean, re.IGNORECASE)
        if addr_match:
            address = addr_match.group(0).replace("Address", "").strip(":- ")

        return f"""{{
    "Name": "{name}",
    "Phone": "{phone}",
    "Email": "{email}",
    "LinkedIn": "{linkedin}",
    "GitHub": "{github}",
    "Date of Birth": "{dob}",
    "Address": "{address}",
    "Document Type": "Resume"
}}"""

    # =====================
    # --- UNKNOWN DOC -----
    # =====================
    else:
        return f"""{{
    "Name": "Not Found",
    "Document Type": "Unknown"
}}"""
