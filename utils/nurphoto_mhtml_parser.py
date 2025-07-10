import pandas as pd
from bs4 import BeautifulSoup

def parse_nurphoto_mhtml(mhtml_file):
    raw_bytes = mhtml_file.read()
    try:
        mhtml_text = raw_bytes.decode("utf-8", errors="ignore")
    except:
        mhtml_text = raw_bytes.decode("latin-1", errors="ignore")

    # Debug: show start of file
    print("File preview:", mhtml_text[:500])

    soup = BeautifulSoup(mhtml_text, "html.parser")

    table = soup.find("table")
    if not table:
        print("No table found in MHTML!")
        # Optionally try to extract data in another way here
        return pd.DataFrame(), "Nurphoto"

    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all("td")
        print("Row cells:", [td.get_text(strip=True) for td in cells])
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
    print("Extracted rows:", len(df))
    return df, "Nurphoto"
