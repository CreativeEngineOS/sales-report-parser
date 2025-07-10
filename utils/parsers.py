```python name=utils/parsers.py
import io

from utils.getty_csv_parser import parse_getty_csv
from utils.getty_statement_parser import parse_getty_statement_csv
# from utils.nurphoto_parser import parse_nurphoto_csv  # Uncomment if supporting Nurphoto

def detect_agency_from_text(text):
    """Detect agency from text content. Expand logic as needed."""
    if "iStock" in text or "Getty" in text:
        return "Getty/iStock"
    elif "Nurphoto" in text:
        return "Nurphoto"
    else:
        return "Unknown"

def parse_pdf(pdf_bytes, agency, with_keywords=False, filename=""):
    """
    Parse the uploaded file based on agency and filename.
    Returns (df, agency) tuple.
    """
    filename_lower = filename.lower()
    # Heuristic: statement-style files have 'statement' or 'dm-' in their name
    if "statement" in filename_lower or "dm-" in filename_lower:
        # New statement format
        return parse_getty_statement_csv(io.BytesIO(pdf_bytes))
    else:
        # Legacy Getty CSV format
        return parse_getty_csv(io.BytesIO(pdf_bytes), with_keywords=with_keywords)
```
