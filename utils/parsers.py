# utils/parsers.py

import pandas as pd
from utils.nurphoto_parser import parse_nurphoto_pdf  # ✅ Add "utils." prefix

def parse_pdf(pdf_bytes, agency):
    if agency == "NurPhoto":
        df = parse_nurphoto_pdf(pdf_bytes)
        return df, "NurPhoto"
    
    return None, agency
