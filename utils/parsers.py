def parse_pdf(pdf_bytes, agency, slug_override=None):
    # In your real implementation, parse based on agency
    dummy_data = {
        "Media Number": ["123456"],
        "Filename": ["example.jpg"],
        "Customer": ["Example Client"],
        "Fee": [3.99],
        "Currency": ["USD"],
        "Your Share": [1.99],
        "Slug": [slug_override or "example-slug"]
    }
    df = pd.DataFrame(dummy_data)
    return df, agency
