import pandas as pd
import io

def parse_getty_csv(file_bytes):
    """
    Parse a Getty/iStock CSV sales report and return a DataFrame and agency name.
    """
    # Decode bytes to string if needed
    if isinstance(file_bytes, bytes):
        text = file_bytes.decode("utf-8")
    else:
        text = file_bytes
    df = pd.read_csv(io.StringIO(text))
    agency = "Getty/iStock"
    return df, agency
