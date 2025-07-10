import pandas as pd
from bs4 import BeautifulSoup

def parse_nurphoto_mhtml(mhtml_bytes):
    soup = BeautifulSoup(mhtml_bytes, "html.parser")
    td_elements = soup.find_all("td")

    records = []
    current = {}

    def get_value(label):
        for idx, td in enumerate(td_elements):
            if td.get_text(strip=True) == label:
                if idx + 1 < len(td_elements):
                    return td_elements[idx + 1].get_text(strip=True)
        return ""

    labels = ["Media Number:", "Filename:", "Original Filename:", "Customer:", "Credit:", "Description:",
              "Fee:", "Your share (%):", "Your share (€):"]

    for idx, td in enumerate(td_elements):
        if td.get_text(strip=True) == "Media Number:":
            if current:
                media_id = current.get("Media Number", "")
                current["Media Link"] = f"https://www.nurphoto.com/photo/{media_id}"
                current["Thumbnail"] = f"<a href='{current['Media Link']}' target='_blank'><img src='https://www.nurphoto.com/photo/{media_id}/picture/photo' width='100'/></a>"
                records.append(current)

            current = {
                "Media Number": get_value("Media Number:"),
                "Filename": get_value("Filename:"),
                "Original Filename": get_value("Original Filename:"),
                "Customer": get_value("Customer:"),
                "Credit": get_value("Credit:"),
                "Description": get_value("Description:"),
                "Fee": 0.0,
                "Currency": "EUR",
                "Your Share (%)": 0,
                "Your Share": 0.0,
                "Agency": "NurPhoto",
                "Media Link": "",
                "Thumbnail": "",
                "Slug?": False
            }

            try:
                fee = get_value("Fee:")
                current["Fee"] = float(fee.replace("€", "").replace(",", ".").strip())
            except:
                current["Fee"] = 0.0

            try:
                pct = get_value("Your share (%):")
                current["Your Share (%)"] = float(pct)
            except:
                current["Your Share (%)"] = 0.0

            try:
                val = get_value("Your share (€):")
                current["Your Share"] = float(val.replace(",", ".").strip())
            except:
                current["Your Share"] = round((current["Fee"] * current["Your Share (%)"] / 100), 2)

    if current:
        media_id = current.get("Media Number", "")
        current["Media Link"] = f"https://www.nurphoto.com/photo/{media_id}"
        current["Thumbnail"] = f"<a href='{current['Media Link']}' target='_blank'><img src='https://www.nurphoto.com/photo/{media_id}/picture/photo' width='100'/></a>"
        records.append(current)

    df = pd.DataFrame(records)
    if "Thumbnail" in df.columns:
        thumb = df.pop("Thumbnail")
        df.insert(0, "Thumbnail", thumb)

    return df
