import pandas as pd
from bs4 import BeautifulSoup

def parse_nurphoto_mhtml(mhtml_bytes):
    soup = BeautifulSoup(mhtml_bytes, "html.parser")
    entries = soup.find_all("b", string="Media Number:")

    records = []

    for entry in entries:
        block = entry.find_parent("td").find_parent("tr") if entry.find_parent("td") else entry.find_parent()
        text = block.get_text(separator="\n", strip=True)

        lines = text.split("\n")
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

        for i, line in enumerate(lines):
            label = line.lower().strip()
            next_val = lines[i + 1].strip() if i + 1 < len(lines) else ""

            if "media number" in label:
                data["Media Number"] = next_val
            elif "filename" in label and not data["Filename"]:
                data["Filename"] = next_val
            elif "original filename" in label:
                data["Original Filename"] = next_val
            elif "customer" in label:
                data["Customer"] = next_val
            elif "credit" in label:
                data["Credit"] = next_val
            elif "description" in label:
                data["Description"] = next_val
            elif "fee" in label:
                fee = next_val.replace("€", "").replace(",", ".").strip()
                try:
                    data["Fee"] = float(fee)
                except:
                    pass
            elif "your share (%)" in label:
                try:
                    data["Your Share (%)"] = int(next_val)
                except:
                    pass
            elif "your share (€" in label:
                share = next_val.replace("€", "").replace(",", ".").strip()
                try:
                    data["Your Share"] = float(share)
                except:
                    pass

        media_id = data["Media Number"]
        data["Media Link"] = f"https://www.nurphoto.com/photo/{media_id}"
        data["Thumbnail"] = f"<img src='https://www.nurphoto.com/photo/{media_id}/picture/photo' width='100'/>"

        records.append(data)

    df = pd.DataFrame(records)
    thumb_col = df.pop("Thumbnail")
    df.insert(0, "Thumbnail", thumb_col)
    return df
