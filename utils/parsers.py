import pandas as pd
import fitz  # For agency detection from text
from utils.nurphoto_parser import parse_nurphoto_pdf
from utils.getty_parser import parse_getty_pdf

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

def parse_pdf(pdf_bytes, agency):
    if agency == "NurPhoto":
        df = parse_nurphoto_pdf(pdf_bytes)
        return df, "NurPhoto"

    elif agency == "Getty/iStock":
        df = parse_getty_pdf(pdf_bytes)
        return df, "Getty/iStock"

    # Future parser
    elif agency == "SIPA USA":
        return None, "SIPA USA (parser not implemented yet)"

    else:
        return None, agency
