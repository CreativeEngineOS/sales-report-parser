# utils/parsers.py

import pandas as pd
from nurphoto_parser import parse_nurphoto_pdf

def parse_pdf(pdf_bytes, agency):
    if agency == "NurPhoto":
        df = parse_nurphoto_pdf(pdf_bytes)
        return df, "NurPhoto"
    
    # Future support for other agencies like SIPA, Getty/iStock
    return None, agency
