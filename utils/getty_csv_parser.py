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

        # Ensure unique column names to avoid assignment errors
        df.columns = pd.io.parsers.ParserBase({'names': df.columns})._maybe_dedup_names(df.columns)

    except Exception as e:
        raise ValueError(f"CSV parsing failed: {str(e)}")

    df.columns = [c.strip() for c in df.columns]
    raw_cols = list(df.columns)

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
        elif col_l == "currency":
            if "Currency" not in col_map.values():  # only map first valid 'currency'
                col_map[col] = "Currency"

    df = df.rename(columns=col_map)

    # Fill in required fields if missing
    for col in ["Media Number", "Description", "Fee", "Currency", "Your Share (%)", "Your Share"]:
        if col not in df.columns:
            df[col] = ""

    df["Media Number"] = df["Media Number"].astype(str)
    df["Agency"] = "Getty/iStock"

    # Clean numeric values
    df["Fee"] = df["Fee"].astype(str).str.replace(",", ".").str.extract(r"([0-9.]+)").astype(float)
    df["Your Share (%)"] = df["Your Share (%)"].astype(str).str.extract(r"([0-9.]+)").astype(float)
    df["Your Share"] = df["Your Share"].astype(str).str.replace(",", ".").str.extract(r"([0-9.]+)").astype(float)

    # Safe thumbnails/links
    df["Media Link"] = df["Media Number"].apply(
        lambda x: f"https://www.istockphoto.com/photo/gm{str(x)}" if str(x).isdigit() else "")
    df["Thumbnail"] = df["Media Number"].apply(
        lambda x: f"<a href='https://www.istockphoto.com/photo/gm{str(x)}' target='_blank'><img src='https://media.gettyimages.com/photos/{str(x)}' width='100'/></a>"
        if str(x).isdigit() else "")

    # Fill remaining NUR-style structure
    df["Filename"] = ""
    df["Original Filename"] = ""
    df["Customer"] = ""
    df["Credit"] = ""
    df["Slug?"] = False

    nur_cols = [
        "Thumbnail", "Media Number", "Filename", "Original Filename", "Customer", "Credit",
        "Description", "Fee", "Currency", "Your Share (%)", "Your Share",
        "Agency", "Media Link", "Slug?"
    ]
    extra_cols = [c for c in df.columns if c not in nur_cols]
    df = df[nur_cols + extra_cols]

    return df
