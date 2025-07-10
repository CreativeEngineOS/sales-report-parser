# utils/parsers.py

import pandas as pd  # ✅ this is essential

def parse_pdf(pdf_bytes, agency):
    # Dummy fallback data structure to test Streamlit integration
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
