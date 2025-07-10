# utils/parsers.py

import pandas as pd  # ✅ Add this line

def parse_pdf(pdf_bytes, agency):
    # This is a dummy dataset for testing the pipeline
    data = {
        "Media Number": ["123456"],
        "Filename": ["example.jpg"],
        "Customer": ["Example Client"],
        "Fee": [3.99],
        "Currency": ["USD"],
        "Your Share": [1.99]
    }

    df = pd.DataFrame(data)
    return df, agency
