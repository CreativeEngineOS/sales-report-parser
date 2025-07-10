import fitz  # PyMuPDF
import pandas as pd
import re

def extract_slug(filename):
    return bool(re.search(r'(BS|BAS)?\d{4,}_[A-Za-z0-9]+_.*__', filename))

def parse_nurphoto_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)

    entries = text.split("Media Number:")[1:]

    # 🔍 DEBUG: Save a sample of what was parsed to check why lines are being skipped
    with open("debug_nurphoto_lines.txt", "w", encoding="utf-8") as debug_out:
        for i, entry in enumerate(entries):
            debug_out.write(f"--- Entry {i+1} ---\n")
            debug_out.write(entry)
            debug_out.write("\n\n")

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
            line_clean = line.lower().replace(" ", "")
            try:
                if "filename:" in line_clean and not data["Filename"]:
                    data["Filename"] = line.split(":")[-1].strip()
                elif "originalfilename:" in line_clean and not data["Original Filename"]:
                    data["Original Filename"] = line.split(":")[-1].strip()
                elif "customer:" in line_clean and not data["Customer"]:
                    data["Customer"] = line.split(":")[-1].strip()
                elif "credit:" in line_clean and not data["Credit"]:
                    data["Credit"] = line.split(":")[-1].strip()
                elif "description:" in line_clean and not data["Description"]:
                    data["Description"] = line.split("Description:")[-1].strip()
                elif "fee:" in line_clean:
                    fee_str = line.split(":")[-1].strip().replace("\u20ac", "").replace(",", ".")
                    data["Fee"] = float(fee_str) if fee_str else 0.0
                elif "yourshare(%):" in line_clean:
                    percent = line.split(":")[-1].strip()
                    data["Your Share (%)"] = int(percent) if percent else 0
                elif "yourshare(\u20ac):" in line_clean:
                    share_str = line.split(":")[-1].strip().replace("\u20ac", "").replace(",", ".")
                    data["Your Share"] = float(share_str) if share_str else 0.0
            except Exception:
                continue

        media_id = data["Media Number"]
        data["Slug?"] = extract_slug(data["Original Filename"])
        data["Media Link"] = f"https://www.nurphoto.com/photo/{media_id}"
        data["Thumbnail Link"] = f"https://www.nurphoto.com/photo/{media_id}/picture/photo"

        records.append(data)

    df = pd.DataFrame(records)
    return df
