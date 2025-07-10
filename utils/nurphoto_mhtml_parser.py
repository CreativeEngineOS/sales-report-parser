import pandas as pd
from bs4 import BeautifulSoup
import re

def parse_nurphoto_mhtml(mhtml_bytes):
    soup = BeautifulSoup(mhtml_bytes, "html.parser")

    media_blocks = soup.find_all("div", class_="contentmedia")
    fee_blocks = soup.find_all("div", class_="contentfees")

    records = []

    for media_div, fee_div in zip(media_blocks, fee_blocks):
        data = {
            "Media Number": "",
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

        for row in media_div.find_all("tr"):
            label = row.find("td", class_="contentmetalabel")
            value = row.find("td", class_="contentmetaval")
            if not label or not value:
                continue
            label_text = label.get_text(strip=True).lower()
            value_text = value.get_text(strip=True)

            if "media number" in label_text:
                data["Media Number"] = value_text
            elif "filename" in label_text and not data["Filename"]:
                data["Filename"] = value_text
            elif "original filename" in label_text:
                data["Original Filename"] = value_text
            elif "customer" in label_text:
                data["Customer"] = value_text
            elif "credit" in label_text:
                data["Credit"] = value_text
            elif "description" in label_text:
                data["Description"] = value_text

        for row in fee_div.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) != 2:
                continue
            label = cells[0].get_text(strip=True).lower()
            value = cells[1].get_text(strip=True)
            if "fee" in label and "share" not in label:
                try:
                    value_clean = re.sub(r"[^0-9,\.]", "", value)
                    data["Fee"] = float(value_clean.replace(",", "."))
                except:
                    data["Fee"] = 0.0
            elif "your share (%)" in label:
                try:
                    data["Your Share (%)"] = float(value.strip())
                except:
                    data["Your Share (%)"] = 0.0
            elif "your share (€" in label:
                try:
                    data["Your Share"] = float(value.replace(",", ".").strip())
                except:
                    data["Your Share"] = 0.0

        media_id = data["Media Number"]
        data["Media Link"] = f"https://www.nurphoto.com/photo/{media_id}"
        data["Thumbnail"] = f"<a href='{data['Media Link']}' target='_blank'><img src='https://www.nurphoto.com/photo/{media_id}/picture/photo' width='100'/></a>"

        records.append(data)

    df = pd.DataFrame(records)
    if "Thumbnail" in df.columns:
        thumb = df.pop("Thumbnail")
        df.insert(0, "Thumbnail", thumb)

    return df
