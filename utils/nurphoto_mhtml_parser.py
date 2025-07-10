import pandas as pd
from bs4 import BeautifulSoup

def parse_nurphoto_mhtml(mhtml_bytes):
    soup = BeautifulSoup(mhtml_bytes, "lxml")
    text = soup.get_text(separator="\n", strip=True)
    entries = text.split("Media Number:")[1:]

    records = []

    for entry in entries:
        lines = entry.strip().split("\n")
        data = {
            "Media Number": lines[0].strip(),
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

        for line in lines[1:]:
            line_lower = line.lower().replace(" ", "")
            if "filename:" in line_lower and not data["Filename"]:
                data["Filename"] = line.split(":")[-1].strip()
            elif "originalfilename:" in line_lower:
                data["Original Filename"] = line.split(":")[-1].strip()
            elif "customer:" in line_lower:
                data["Customer"] = line.split(":")[-1].strip()
            elif "credit:" in line_lower:
                data["Credit"] = line.split(":")[-1].strip()
            elif "description:" in line_lower:
                data["Description"] = line.split("Description:")[-1].strip()
            elif "fee:" in line_lower:
                fee = line.split(":")[-1].replace("€", "").replace(",", ".").strip()
                data["Fee"] = float(fee) if fee else 0.0
            elif "yourshare(%):" in line_lower:
                pct = line.split(":")[-1].strip()
                data["Your Share (%)"] = int(pct) if pct else 0
            elif "yourshare(€):" in line_lower:
                share = line.split(":")[-1].replace("€", "").replace(",", ".").strip()
                data["Your Share"] = float(share) if share else 0.0

        media_id = data["Media Number"]
        data["Media Link"] = f"https://www.nurphoto.com/photo/{media_id}"
        data["Thumbnail"] = f"<img src='https://www.nurphoto.com/photo/{media_id}/picture/photo' width='100'/>"

        records.append(data)

    df = pd.DataFrame(records)
    thumb_col = df.pop("Thumbnail")
    df.insert(0, "Thumbnail", thumb_col)
    return df
