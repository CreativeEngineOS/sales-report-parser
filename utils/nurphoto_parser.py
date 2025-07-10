import fitz  # PyMuPDF
import pandas as pd
import re

def extract_slug(filename):
    # Return True if the filename has an internal slug format
    return bool(re.search(r'(BS|BAS)?\d{4,}_[A-Za-z0-9]+_.*__', filename))

def parse_nurphoto_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)

    # Split entries using "Media Number:" as the key delimiter
    entries = text.split("Media Number:")[1:]  # drop header

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
            "Your Share": 0.0
        }

        for line in lines[1:]:
            if line.startswith("Filename:"):
                data["Filename"] = line.split("Filename:")[1].strip()
            elif line.startswith("Original Filename:"):
                data["Original Filename"] = line.split("Original Filename:")[1].strip()
            elif line.startswith("Customer:"):
                data["Customer"] = line.split("Customer:")[1].strip()
            elif line.startswith("Credit:"):
                data["Credit"] = line.split("Credit:")[1].strip()
            elif line.startswith("Description:"):
                data["Description"] = line.split("Description:")[1].strip()
            elif line.startswith("Fee:"):
                fee_str = line.split("Fee:")[1].strip().replace("€", "").replace(",", ".")
                data["Fee"] = float(fee_str)
            elif line.startswith("Your share (%):"):
                data["Your Share (%)"] = int(line.split(":")[1].strip())
            elif line.startswith("Your share (€):"):
                share_str = line.split(":")[1].strip().replace("€", "").replace(",", ".")
                data["Your Share"] = float(share_str)

        media_id = data["Media Number"]
        data["Slug?"] = extract_slug(data["Original Filename"])
        data["Media Link"] = f"https://www.nurphoto.com/photo/{media_id}"
        data["Thumbnail Link"] = f"https://www.nurphoto.com/photo/{media_id}/picture/photo"

        records.append(data)

    df = pd.DataFrame(records)
    return df
