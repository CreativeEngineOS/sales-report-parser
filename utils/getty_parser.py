import io
import pdfplumber
import pandas as pd

def parse_getty_pdf(pdf_bytes):
    rows = []

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        with open("debug_getty_table.txt", "w", encoding="utf-8") as dbg:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    dbg.write(f"--- Page {page.page_number} ---\n")
                    for row in table:
                        dbg.write(str(row) + "\n")
                    dbg.write("\n")

                    headers = [h.strip() if h else f"col{i}" for i, h in enumerate(table[0])]
                    for row in table[1:]:
                        if len(row) < len(headers):
                            continue  # skip malformed rows
                        record = dict(zip(headers, row))
                        rows.append(record)

    records = []

    for item in rows:
        try:
            fee_str = item.get("License Fee", item.get("Amount", "0")).replace("$", "").strip()
            royalty_str = item.get("Royalty", "0").replace("$", "").strip()

            media_number = item.get("Asset ID") or item.get("Asset Number") or item.get("ID") or ""
            description = item.get("Title") or item.get("Description") or ""
            sale_date = item.get("Sales Date") or item.get("Date") or ""

            data = {
                "Media Number": media_number.strip(),
                "Description": description.strip(),
                "Sale Date": sale_date.strip(),
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
