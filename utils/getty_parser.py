import pdfplumber
import pandas as pd

def parse_getty_pdf(pdf_bytes):
    records = []

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                headers = table[0]
                for row in table[1:]:
                    row_dict = dict(zip(headers, row))

                    media_number = row_dict.get("Asset ID") or row_dict.get("Image ID") or ""
                    description = row_dict.get("Description") or ""
                    date = row_dict.get("Sale Date") or row_dict.get("Date") or ""
                    fee = row_dict.get("License Fee") or row_dict.get("Gross Fee") or ""
                    royalty = row_dict.get("Royalty") or row_dict.get("Your Share") or ""

                    try:
                        fee = float(fee.replace("$", "").replace(",", "").strip()) if fee else 0.0
                    except:
                        fee = 0.0
                    try:
                        royalty = float(royalty.replace("$", "").replace(",", "").strip()) if royalty else 0.0
                    except:
                        royalty = 0.0

                    records.append({
                        "Media Number": media_number,
                        "Description": description,
                        "Sale Date": date,
                        "Fee": fee,
                        "Currency": "USD",
                        "Your Share (%)": 0,  # Not typically provided
                        "Your Share": royalty,
                        "Agency": "Getty/iStock"
                    })

    return pd.DataFrame(records)
