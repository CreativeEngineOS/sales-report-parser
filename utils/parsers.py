import fitz  # PyMuPDF

def detect_agency_from_text(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    first_page_text = doc[0].get_text().lower()

    if "nurphoto agency" in first_page_text:
        return "NurPhoto"
    elif "getty" in first_page_text or "istock" in first_page_text:
        return "Getty/iStock"
    elif "sipa" in first_page_text:
        return "SIPA USA"
    else:
        return "Unknown"
