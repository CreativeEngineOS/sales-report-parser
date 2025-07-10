import pandas as pd
from bs4 import BeautifulSoup
import re

def parse_nurphoto_mhtml(mhtml_bytes):
    soup = BeautifulSoup(mhtml_bytes, "html.parser")
    td_elements = soup.find_all("td")

    records = []
    current = {}

    def get_value(label):
        for idx, td in enumerate(td_elements):
            if td.get_text(strip=True) == label:
                if idx + 1 < len(td_elements):
                    val = td_elements[idx + 1].get_text(strip=True)
                    return re.sub(r'=\r?\n', '', val)  # clean description/values
        return ""

    for idx, td in enumerate(td_elements):
        if td.get_text(strip=True) == "Media Number:":
            if current:
                media_id = current.get("Media Number", "")
                current["Media Link"] = f"https://www.nurphoto.com/photo/{media_id}"
                current["Thumbnail"] = f"<a href='{current['Media Link']}' target='_blank'><img src='https://www.nurphoto.com/photo/{media_id}/picture/photo' width='100'/></a>"
                records.append(current)

            fee_val = get_value("Fee:")
            fee_match = re.search(r"([0-9]{1,3}[,.]?[0-9]{0,2})", fee_val)
            fee_clean = float(fee_match.group(1).replace(",", ".")) if fee_match else 0.0

            share_pct = get_value("Your share (%):")
            share_val = get_value("Your share (€):")

            try:
                share_pct_float = float(share_pct)
            except:
                share_pct_float = 0.0

            try:
                share_val_float = float(share_val.replace(",", "."))
            except:
                share_val_float = round((fee_clean * share_pct_float / 100), 2)

            current = {
                "Media Number": get_value("Media Number:"),
                "Filename": get_value("Filename:"),
                "Original Filename": get_value("Original Filename:"),
                "Customer": get_value("Customer:"),
                "Credit": get_value("Credit:"),
                "Description": get_value("Description:"),
                "Fee": fee_clean,
                "Currency": "EUR",
                "Your Share (%)": share_pct_float,
                "Your Share": share_val_float,
                "Agency": "NurPhoto",
                "Media Link": "",
                "Thumbnail": "",
                "Slug?": False
            }

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
