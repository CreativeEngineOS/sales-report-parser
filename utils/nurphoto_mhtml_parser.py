import pandas as pd
from bs4 import BeautifulSoup
import re

def parse_nurphoto_mhtml(mhtml_bytes):
    soup = BeautifulSoup(mhtml_bytes, "html.parser")
    rows = soup.find_all("tr")

    records = []
    current = {}

    def clean(val):
        return re.sub(r'=\r?\n', '', val).strip()

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 2:
            continue

        label = cells[0].get_text(strip=True).lower().replace("\xa0", "").rstrip(":").strip()
        value = clean(cells[1].get_text(strip=True))

        if "media number" in label:
            if current:  # flush previous
                if "Media Number" in current:
                    media_id = current["Media Number"]
                    current["Media Link"] = f"https://www.nurphoto.com/photo/{media_id}"
                    current["Thumbnail"] = f"<img src='https://www.nurphoto.com/photo/{media_id}/picture/photo' width='100'/>"
                    records.append(current)
            current = {
                "Media Number": value,
                "Filename": "",
                "Original Filename": "",
                "Customer": "",
                "Credit": "",
                "Description": "",
                "Fee": 0.0,
                "Currency": "EUR",
                "Your Share (%)": 0,
                "Your Share": 0.0,
                "Agency": "NurPhoto",
                "Media Link": "",
                "Thumbnail": "",
                "Slug?": False
            }

        elif "filename" in label and not current.get("Filename"):
            current["Filename"] = value
        elif "original filename" in label:
            current["Original Filename"] = value
        elif "customer" in label:
            current["Customer"] = value
        elif "credit" in label:
            current["Credit"] = value
        elif "description" in label:
            current["Description"] = value
        elif "fee" in label and "share" not in label:
            try:
                current["Fee"] = float(value.replace("€", "").replace(",", "."))
            except:
                current["Fee"] = 0.0
        elif "your share (%)" in label:
            try:
                current["Your Share (%)"] = int(value)
            except:
                current["Your Share (%)"] = 0
        elif "your share (€" in label:
            try:
                current["Your Share"] = float(value.replace("€", "").replace(",", "."))
            except:
                current["Your Share"] = 0.0

    if current and "Media Number" in current:
        media_id = current["Media Number"]
        current["Media Link"] = f"https://www.nurphoto.com/photo/{media_id}"
        current["Thumbnail"] = f"<img src='https://www.nurphoto.com/photo/{media_id}/picture/photo' width='100'/>"
        records.append(current)

    df = pd.DataFrame(records)

    if "Thumbnail" in df.columns:
        thumb_col = df.pop("Thumbnail")
        df.insert(0, "Thumbnail", thumb_col)

    return df
