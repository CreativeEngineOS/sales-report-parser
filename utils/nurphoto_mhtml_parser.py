import pandas as pd
from bs4 import BeautifulSoup

def parse_nurphoto_mhtml(mhtml_file):
    """
    Parse Nurphoto MHTML sales report from a file-like object (BytesIO).
    Returns (df, agency).
    """
    # Read the raw bytes
    raw_bytes = mhtml_file.read()
    # Decode to text
    mhtml_text = raw_bytes.decode("utf-8", errors="ignore")
    # Parse with BeautifulSoup (if HTML structure is present)
    soup = BeautifulSoup(mhtml_text, "html.parser")

    # Example extraction - adjust based on actual Nurphoto MHTML structure
    # This is a stub: replace with real parsing logic
    rows = []
    table = soup.find("table")
    if table:
        for tr in table.find_all("tr"):
            cells = tr.find_all("td")
            if len(cells) >= 3:
                filename = cells[0].get_text(strip=True)
                date = cells[1].get_text(strip=True)
                amount = cells[2].get_text(strip=True)
                thumbnail = cells[3].get_text(strip=True) if len(cells) > 3 else ""
                rows.append({
                    "Filename": filename,
                    "Date": date,
                    "Amount": amount,
                    "Thumbnail": thumbnail,
                })

    df = pd.DataFrame(rows)
    agency = "Nurphoto"
    return df, agency
