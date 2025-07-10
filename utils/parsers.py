import pandas as pd
from utils.nurphoto_parser import parse_nurphoto_pdf
from utils.getty_parser import parse_getty_pdf  # this will be created

def parse_pdf(pdf_bytes, agency):
    if agency == "NurPhoto":
        df = parse_nurphoto_pdf(pdf_bytes)
        return df, "NurPhoto"

    elif agency == "Getty/iStock":
        df = parse_getty_pdf(pdf_bytes)
        return df, "Getty/iStock"

    # Placeholder for future agencies like SIPA
    return None, agency
