import pandas as pd

def parse_nurphoto_mhtml(mhtml_bytes):
    """
    Parse Nurphoto MHTML sales report from raw bytes.
    Returns (df, agency)
    """
    # Decode bytes to text
    mhtml_text = mhtml_bytes.decode("utf-8", errors="ignore")

    # TODO: Implement actual parsing logic for Nurphoto MHTML content
    # For now, create a dummy DataFrame
    df = pd.DataFrame({
        "Filename": [],
        "Date": [],
        "Amount": [],
        "Thumbnail": [],
    })

    agency = "Nurphoto"
    return df, agency
