import pandas as pd
import csv
import io
import re

def parse_getty_csv(csv_file, with_keywords=False):
    try:
        content = csv_file.read()
        if isinstance(content, bytes):
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                text = content.decode("utf-16")
        else:
            text = content

        sample = text[:2048]
        delimiter = "\t" if "\t" in sample else csv.Sniffer().sniff(sample).delimiter

        df = pd.read_csv(io.StringIO(text), delimiter=delimiter)

        # Safely deduplicate column names
        seen = {}
        new_cols = []
        for col in df.columns:
            if col not in seen:
                seen[col] = 1
                new_cols.append(col)
            else:
                seen[col] += 1
                new_cols.append(f"{col}_{seen[col]}")
        df.columns = new_cols

    except Exception as e:
        raise ValueError(f"CSV parsing failed: {str(e)}")

    df.columns = [c.strip() for c in df.columns]
    raw_cols = list(df.columns)

    # Check for duplicate columns
    if pd.Series(df.columns).duplicated().any():
        print("Warning: Duplicate columns detected and will be renamed.")

    # Check for duplicate index labels and force reset
    if not df.index.is_unique:
        print("Warning: Duplicate DataFrame index detected. Resetting index.")
        df = df.reset_index(drop=True)

    # Optionally drop duplicate rows based on Media Number
    if "Media Number" in df.columns and df["Media Number"].duplicated().any():
        print("Warning: Duplicate Media Number values detected. Keeping first occurrence.")
        df = df.drop_duplicates(subset=["Media Number"], keep="first").reset_index(drop=True)

    col_map = {}
    for col in raw_cols:
        col_l = col.lower()
        if "asset number" in col_l or "asset id" in col_l:
            col_map[col] = "Media Number"
        elif "description" in col_l or "title" in col_l:
            col_map[col] = "Description"
        elif col_l == "fee":
            col_map[col] = "Fee"
        elif "gross royalty" in col_l:
            col_map[col] = "Your Share"
        elif "royalty rate" in col_l or "your share (%)" in col_l:
            col_map[col] = "Your Share (%)"
        elif col_l == "currency" and "Currency" not in col_map.values():
            col_map[col] = "Currency"

    df = df.rename(columns=col_map)

    for col in ["Media Number", "Description", "Fee", "Currency", "Your Share (%)", "Your Share"]:
        if col not in df.columns:
            df[col] = ""

    df["Media Number"] = df["Media Number"].astype(str)
    df["Agency"] = "Getty/iStock"

    df["Fee"] = df["Fee"].astype(str).str.replace(",", ".").str.extract(r"([0-9.]+)").astype(float)
    df["Your Share (%)"] = df["Your Share (%)"].astype(str).str.extract(r"([0-9.]+)").astype(float)
    df["Your Share"] = df["Your Share"].astype(str).str.replace(",", ".").str.extract(r"([0-9.]+)").astype(float)

    # FINAL index check before assignment
    if not df.index.is_unique:
        print("Error: DataFrame index is still not unique before assignment. Resetting index again.")
        df = df.reset_index(drop=True)

    # Assign Media Link and Thumbnail columns safely
    df["Media Link"] = df["Media Number"].apply(
        lambda x: f"https://www.istockphoto.com/photo/gm{str(x)}" if str(x).isdigit() else "")
    df["Thumbnail"] = df["Media Number"].apply(
        lambda x: f"<a href='https://www.istockphoto.com/photo/gm{str(x)}' target='_blank'><img src='https://media.gettyimages.com/photos/{str(x)}' width='100'/></a>"
        if str(x).isdigit() else "")

    df["Filename"] = ""
    df["Original Filename"] = ""
    df["Customer"] = ""
    df["Credit"] = ""
    df["Slug?"] = False

    nur_cols = [
        "Thumbnail", "Media Number", "Filename", "Original Filename", "Customer", "Credit",
        "Description", "Fee", "Currency", "Your Share (%)", "Your Share", "Agency", "Media Link", "Slug?"
    ]
    extra_cols = [c for c in df.columns if c not in nur_cols]
    df = df[nur_cols + extra_cols]

    return df, "Getty/iStock"
