from utils.getty_parser import parse_getty_csv
from utils.nurphoto_mhtml_parser import parse_nurphoto_mhtml
from utils.editorialfootage_mhtml_parser import parse_editorialfootage_mhtml

def detect_agency_from_text(text):
    text_lower = text.lower()
    if "istock" in text_lower or "getty" in text_lower:
        return "Getty/iStock"
    elif "nurphoto" in text_lower:
        return "Nurphoto"
    elif "editorialfootage" in text_lower or "editorial footage" in text_lower:
        return "EditorialFootage"
    else:
        return "Unknown"

def parse_pdf(file_bytes, agency, filename=""):
    """
    Unified parser interface for sales report files.
    Returns (df, agency) where df is a pandas DataFrame and agency is a string.
    """
    filename_lower = filename.lower()
    # Handle MHTML files
    if filename_lower.endswith(".mhtml"):
        if agency == "Nurphoto":
            return parse_nurphoto_mhtml(file_bytes)
        elif agency == "EditorialFootage":
            return parse_editorialfootage_mhtml(file_bytes)
        else:
            raise ValueError("Unsupported MHTML agency for file: " + filename)
    # Handle CSV files for Getty/iStock only
    if filename_lower.endswith(".csv"):
        if agency == "Getty/iStock":
            return parse_getty_csv(file_bytes)
        else:
            raise ValueError("Unsupported agency for CSV file: " + agency)
    # Unsupported file type
    raise ValueError("Unsupported file type: " + filename)
