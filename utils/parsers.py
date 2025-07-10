import io

from utils.getty_csv_parser import parse_getty_csv
from utils.getty_statement_parser import parse_getty_statement_csv
from utils.nurphoto_mhtml_parser import parse_nurphoto_mhtml
from utils.editorialfootage_mhtml_parser import parse_editorialfootage_mhtml

def detect_agency_from_text(text):
    """
    Detect the agency from the given text.
    Extend this function for more robust detection as needed.
    """
    text_lower = text.lower()
    if "istock" in text_lower or "getty" in text_lower:
        return "Getty/iStock"
    elif "nurphoto" in text_lower:
        return "Nurphoto"
    elif "editorialfootage" in text_lower or "editorial footage" in text_lower:
        return "EditorialFootage"
    else:
        return "Unknown"

def parse_pdf(pdf_bytes, agency, with_keywords=False, filename=""):
    """
    Unified parser interface for sales report files.
    Returns (df, agency) where df is a pandas DataFrame and agency is a string.
    """
    filename_lower = filename.lower()
    # Handle MHTML files
    if filename_lower.endswith(".mhtml"):
        if agency == "Nurphoto":
            return parse_nurphoto_mhtml(io.BytesIO(pdf_bytes))
        elif agency == "EditorialFootage":
            return parse_editorialfootage_mhtml(io.BytesIO(pdf_bytes))
        else:
            raise ValueError("Unsupported MHTML agency for file: " + filename)
    # Handle CSV and TXT files for Getty/iStock only
    if filename_lower.endswith(".csv") or filename_lower.endswith(".txt"):
        if agency == "Getty/iStock":
            if "statement" in filename_lower or "dm-" in filename_lower:
                return parse_getty_statement_csv(io.BytesIO(pdf_bytes))
            else:
                return parse_getty_csv(io.BytesIO(pdf_bytes), with_keywords=with_keywords)
        else:
            raise ValueError("Unsupported agency for CSV/TXT file: " + agency)
    # Unsupported file type
    raise ValueError("Unsupported file type: " + filename)
