import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_istock_keywords(asset_id):
    url = f"https://www.istockphoto.com/photo/gm{asset_id}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            meta = soup.find("meta", {"name": "keywords"})
            return meta["content"] if meta else ""
    except Exception:
        return ""

def parse_getty_csv(csv_bytes, with_keywords=False):
    # Peek to detect delimiter
    sample = csv_bytes.read(1024).decode(errors='ignore')
    sep = '\t' if '\t' in sample else ','

    csv_bytes.seek(0)
    df = pd.read_csv(csv_bytes, sep=sep)
    records = []

    for _, row in df.iterrows():
        try:
            fee = float(str(row.get("License Fee in USD", 0)).replace("$", "").strip() or 0)
            royalty = float(str(row.get("Gross Royalty in USD", 0)).replace("$", "").strip() or 0)
            asset_id = str(row.get("Asset Number", "")).strip()
            description = str(row.get("Asset Description", "")).strip()
            sale_date = str(row.get("Sales Date", row.get("Invoice Date", ""))).strip()
            keywords = fetch_istock_keywords(asset_id) if with_keywords else ""

            data = {
                "Media Number": asset_id,
                "Description": description,
                "Sale Date": sale_date,
                "Fee": fee,
                "Currency": "USD",
                "Your Share (%)": round((royalty / fee) * 100, 2) if fee else 0,
                "Your Share": royalty,
                "Agency": "Getty/iStock",
                "Media Link": f"https://www.istockphoto.com/photo/gm{asset_id}",
                "Thumbnail": f"<img src='https://www.istockphoto.com/photo/gm{asset_id}' width='100'/>",
                "Slug?": False,
                "Keywords": keywords
            }

            records.append(data)
        except Exception:
            continue

    return pd.DataFrame(records)
