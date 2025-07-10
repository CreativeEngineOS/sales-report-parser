import pandas as pd
import csv
import io
import re

def parse_getty_csv(csv_file, with_keywords=False):
    # Try reading with auto-detection of delimiter and encoding
    try:
        content = csv_file.read()
        if isinstance(content, bytes):
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                text = content.decode("utf-16")  # fallback if utf-8 fails
        else:
            text = content

        # Use csv.Sniffer to detect delimiter
        sample = text[:2048]
        dialect = csv.Sniffer().sniff(sample)
        delimiter = dialect.delimiter

        df = pd.read_csv(io.StringIO(text), delimiter=delimiter)

    except Exception as e:
        raise ValueError(f"CSV parsing failed: {str(e)}")

    # Debug fallback: print columns for inspection if something breaks
    expected_raw = ['Asset ID', 'Title', 'Download Date', 'License Fee', 'Currency', 'Royalty Rate', 'Royalty Amount']
    missing = [col for col in expected_raw if col not in df.columns]
    if missing:
        raise KeyError(f"Missing expected columns in iStock/CSV: {missing}. Found columns: {list(df.columns)}")

    # Normalize/rename expected Getty/iStock fields
    df = df.rename(columns={
        'Asset ID': 'Media Number',
        'Title': 'Description',
        'Download Date': 'Sale Date',
        'License Fee': 'Fee',
        'Currency': 'Currency',
        'Royalty Rate': 'Your Share (%)',
        'Royalty Amount': 'Your Share'
    })

    df['Media Number'] = df['Media Number'].astype(str)
    df['Agency'] = 'Getty/iStock'

    # Media Link and Thumbnail
    df['Media Link'] = df['Media Number'].apply(
        lambda x: f"https://www.istockphoto.com/photo/gm{x}" if x.isnumeric() else "")
    df['Thumbnail'] = df['Media Number'].apply(
        lambda x: f"<a href='https://www.istockphoto.com/photo/gm{x}' target='_blank'><img src='https://media.gettyimages.com/photos/{x}' width='100'/></a>"
        if x.isnumeric() else "")

    # Required Nur-style columns
    df['Filename'] = ""
    df['Original Filename'] = ""
    df['Customer'] = ""
    df['Credit'] = ""
    df['Slug?'] = False

    # Ensure Fee and Royalty are floats
    df['Fee'] = df['Fee'].astype(str).str.replace(",", ".").str.extract(r"([0-9.]+)").astype(float)
    df['Your Share (%)'] = df['Your Share (%)'].astype(str).str.extract(r"([0-9.]+)").astype(float)
    df['Your Share'] = df['Your Share'].astype(str).str.replace(",", ".").str.extract(r"([0-9.]+)").astype(float)

    # Add placeholder if Keywords enabled
    if with_keywords:
        df['Keywords'] = df.get('Keywords', '')

    # Final column order (Nur standard)
    final_columns = [
        'Thumbnail', 'Media Number', 'Filename', 'Original Filename', 'Customer', 'Credit',
        'Description', 'Fee', 'Currency', 'Your Share (%)', 'Your Share',
        'Agency', 'Media Link', 'Slug?'
    ]
    if with_keywords:
        final_columns.append('Keywords')

    df = df[final_columns]
    return df
