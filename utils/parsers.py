# utils/parsers.py

import pandas as pd

def parse_pdf(pdf_bytes, agency):
    # This is a placeholder — implement agency-specific logic later
    dummy_data = {
        "Media Number": ["123456"],
        "Filename": ["example.jpg"],
        "Customer": ["Example Client"],
        "Fee": [3.99],
        "Currency": ["USD"],
        "Your Share": [1.99],
    }

    df = pd.DataFrame(dummy_data)
    return df, agency
