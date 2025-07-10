import pandas as pd

def parse_getty_csv(csv_bytes):
    df = pd.read_csv(csv_bytes)

    records = []

    for _, row in df.iterrows():
        try:
            fee = float(str(row.get("License Fee in USD", 0)).replace("$", "").strip() or 0)
            royalty = float(str(row.get("Gross Royalty in USD", 0)).replace("$", "").strip() or 0)
            asset_id = str(row.get("Asset Number", "")).strip()
            description = str(row.get("Asset Description", "")).strip()
            sale_date = str(row.get("Sales Date", "")).strip()

            data = {
                "Media Number": asset_id,
                "Description": description,
                "Sale Date": sale_date,
                "Fee": fee,
                "Currency": "USD",
                "Your Share (%)": round((royalty / fee) * 100, 2) if fee else 0,
                "Your Share": royalty,
                "Agency": "Getty/iStock",
                "Media Link": f"https://www.istockphoto.com/photo/{asset_id}",
                "Thumbnail": f"<img src='https://www.istockphoto.com/photo/{asset_id}' width='100'/>",
                "Slug?": False
            }

            records.append(data)
        except Exception:
            continue

    return pd.DataFrame(records)
