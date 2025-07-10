import pandas as pd
import io

def parse_getty_statement_csv(csv_file):
    try:
        # Read file contents, handle bytes or str
        content = csv_file.read()
        if isinstance(content, bytes):
            text = content.decode("utf-8")
        else:
            text = content

        # Load CSV with comma delimiter
        df = pd.read_csv(io.StringIO(text))

    except Exception as e:
        raise ValueError(f"CSV parsing failed: {str(e)}")

    # Nurphoto-style column order
    nur_cols = [
        "Thumbnail", "Media Number", "Filename", "Original Filename", "Customer", "Credit",
        "Description", "Fee", "Currency", "Your Share (%)", "Your Share",
        "Agency", "Media Link", "Slug?"
    ]

    # Column mapping from statement to nurphoto style
    col_map = {
        "Filename": "Filename",
        "Contract Name": "Description",
        "Contributors Net Payment": "Fee",
        "Exchange Rate": "Currency",
        "Contributor Percentage": "Your Share (%)",
        "US Contributors Share": "Your Share",
    }

    # Create nur_cols from mapped columns or empty if missing
    for nur_col in nur_cols:
        if nur_col not in df.columns:
            # Map from CSV if possible, else empty
            orig_col = [k for k, v in col_map.items() if v == nur_col]
            if orig_col and orig_col[0] in df.columns:
                df[nur_col] = df[orig_col[0]]
            else:
                df[nur_col] = ""

    # Agency column
    df["Agency"] = "Getty/iStock"

    # Media Number: Use Contract ID, fallback to Contact ID
    if "Contract ID" in df.columns:
        df["Media Number"] = df["Contract ID"].astype(str)
    elif "Contact ID" in df.columns:
        df["Media Number"] = df["Contact ID"].astype(str)
    else:
        df["Media Number"] = ""

    # Reset index before assignment (avoids pandas index bugs)
    df = df.reset_index(drop=True)

    # Media Link & Thumbnail (using Media Number if numeric)
    df["Media Link"] = df["Media Number"].apply(
        lambda x: f"https://www.istockphoto.com/photo/gm{str(x)}" if str(x).isdigit() else ""
    )
    df["Thumbnail"] = df["Media Number"].apply(
        lambda x: f"<a href='https://www.istockphoto.com/photo/gm{str(x)}' target='_blank'><img src='https://media.gettyimages.com/photos/{str(x)}' width='100'/></a>"
        if str(x).isdigit() else ""
    )

    # Other fields
    df["Filename"] = df["Filename"].astype(str)
    df["Original Filename"] = ""
    df["Customer"] = ""
    df["Credit"] = ""
    df["Slug?"] = False

    # Fee, Your Share, Your Share (%) as float
    for col in ["Fee", "Your Share", "Your Share (%)"]:
        df[col] = df[col].astype(str).str.replace(",", ".").str.extract(r"([0-9.]+)").astype(float)

    # Reorder columns to Nurphoto-style, append extras at the end
    extra_cols = [c for c in df.columns if c not in nur_cols]
    df = df[nur_cols + extra_cols]

    return df, "Getty/iStock"
