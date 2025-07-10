import pandas as pd
from bs4 import BeautifulSoup

def parse_nurphoto_mhtml(mhtml_bytes):
    soup = BeautifulSoup(mhtml_bytes, "html.parser")
    rows = soup.find_all("tr")

    records = []
    current = {}

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 2:
            continue

        label = cells[0].get_text(strip=True).lower().replace("\xa0", "").rstrip(":").strip()
        value = cells[1].get_text(strip=True)

        if "media number" in label:
            if current:  # flush previous
                if "Media Number" in current:
                    current["Media Link"] = f"https://www.nurphoto.com/photo/{current['Media Number']}"
                    current["Thumbnail"] = f"<img src='https://www.nurphoto.com/photo/{current['Media Number']}/picture/photo' width='100'/>"
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
        elif "filename" == label and not current.get("Filename"):
            current["Filename"] = value
        elif "original filename" == label:
            current["Original Filename"] = value
        elif "customer" == label:
            current["Customer"] = value
        elif "credit" == label:
            current["Credit"] = value
        elif "description" == label:
            current["Description"] = value
        elif "fee" == label:
            try:
                current["Fee"] = float(value.replace("€", "").replace(",", "."))
            except:
                pass
        elif "your share (%)" in label:
            try:
                current["Your Share (%)"] = int(value)
            except:
                pass
        elif "your share (€" in label:
            try:
                current["Your Share"] = float(value.replace("€", "").replace(",", "."))
            except:
                pass

    if current and "Media Number" in current:
        current["Media Link"] = f"https://www.nurphoto.com/photo/{current['Media Number']}"
        current["Thumbnail"] = f"<img src='https://www.nurphoto.com/photo/{current['Media Number']}/picture/photo' width='100'/>"
        records.append(current)

    df = pd.DataFrame(records)
    if "Thumbnail" in df.columns:
        thumb_col = df.pop("Thumbnail")
        df.insert(0, "Thumbnail", thumb_col)
    return df
