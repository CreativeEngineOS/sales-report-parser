import io
import pandas as pd
import fitz  # PyMuPDF for PDF text parsing
from utils.nurphoto_parser import parse_nurphoto_pdf
from utils.getty_parser import parse_getty_pdf
from utils.getty_csv_parser import parse_getty_csv
# from utils.sipa_parser import parse_sipa_pdf
# from utils.alamy_parser import parse_alamy_pdf
# from utils.adobe_parser import parse_adobe_pdf

def detect_agency_from_text(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    first_page_text = doc[0].get_text().lower()

    if "nurphoto agency" in first_page_text:
        return "NurPhoto"
    elif "getty" in first_page_text or "istock" in first_page_text:
        return "Getty/iStock"
    elif "sipa" in first_page_text:
        return "SIPA USA"
    elif "alamy" in first_page_text:
        return "Alamy"
    elif "adobe" in first_page_text:
        return "Adobe"
    else:
        return "Unknown"

def parse_pdf(pdf_bytes, agency, with_keywords=False):
    if agency == "NurPhoto":
        return parse_nurphoto_pdf(pdf_bytes), "NurPhoto"

    elif agency == "Getty/iStock":
        # Detect if it's a CSV by checking for commas or PK (ZIP signature)
        if pdf_bytes[:4] == b'PK\x03\x04' or b',' in pdf_bytes[:1000]:
            return parse_getty_csv(io.BytesIO(pdf_bytes), with_keywords=with_keywords), "Getty/iStock"
        else:
            return parse_getty_pdf(pdf_bytes), "Getty/iStock"

    elif agency == "SIPA USA":
        return None, "SIPA USA (parser not implemented yet)"

    elif agency == "Alamy":
        return None, "Alamy (parser not implemented yet)"

    elif agency == "Adobe":
        return None, "Adobe (parser not implemented yet)"

    else:
        return None, agency
