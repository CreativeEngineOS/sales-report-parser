# utils/parsers.py

import pandas as pd  # ✅ REQUIRED or you'll get NameError

def parse_pdf(pdf_bytes, agency):
    # Dummy fallback data until real parsing is implemented
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
