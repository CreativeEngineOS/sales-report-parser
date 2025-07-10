import pandas as pd

def parse_pdf(pdf_bytes):
    # Placeholder parser for now
    dummy_data = {
        "Media Number": ["123456"],
        "Filename": ["example.jpg"],
        "Customer": ["Example Client"],
        "Fee": [3.99],
        "Currency": ["USD"],
        "Your Share": [1.99]
    }
    df = pd.DataFrame(dummy_data)
    return df, "DummyAgency"
