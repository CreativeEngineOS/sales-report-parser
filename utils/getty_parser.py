import io
import pdfplumber
import pandas as pd

def parse_getty_pdf(pdf_bytes):
    rows = []

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                headers = [h.strip() for h in table[0]]
                for row in table[1:]:
                    if len(row) < len(headers):
                        continue  # skip malformed rows
                    record = dict(zip(headers, row))
                    rows.append(record)

    records = []

    for item in rows:
        try:
            fee_str = item.get("License Fee", "0").replace("$", "").strip()
            royalty_str = item.get("Royalty", "0").replace("$", "").strip()

            data = {
                "Media Number": item.get("Asset ID", item.get("Asset Number", "")).strip(),
                "Description": item.get("Title", item.get("Description", "")).strip(),
                "Sale Date": item.get("Sales Date", "").strip(),
                "Fee": float(fee_str) if fee_str else 0.0,
                "Currency": "USD",
                "Your Share (%)": 0,
                "Your Share": float(royalty_str) if royalty_str else 0.0,
                "Agency": "Getty/iStock",
                "Media Link": "",
                "Thumbnail": ""
            }

            records.append(data)
        except Exception:
            continue

    return pd.DataFrame(records)
