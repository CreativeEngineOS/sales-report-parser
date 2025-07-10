import pandas as pd
from bs4 import BeautifulSoup
import re

def parse_nurphoto_mhtml(mhtml_bytes):
    soup = BeautifulSoup(mhtml_bytes, "html.parser")
    td_elements = soup.find_all("td")

    records = []
    current = {}
    record_blocks = []

    # Step 1: group into blocks by "Media Number:"
    block = []
    for td in td_elements:
        if td.get_text(strip=True) == "Media Number:" and block:
            record_blocks.append(block)
            block = []
        block.append(td)
    if block:
        record_blocks.append(block)

    # Step 2: parse each block independently
    def extract_value(block, label):
        for idx, td in enumerate(block):
            if td.get_text(strip=True) == label:
                if idx + 1 < len(block):
                    val = block[idx + 1].get_text(strip=True)
                    return re.sub(r'=\r?\n', '', val)
        return ""

    for block in record_blocks:
        media_number = extract_value(block, "Media Number:")
        filename = extract_value(block, "Filename:")
        original_filename = extract_value(block, "Original Filename:")
        customer = extract_value(block, "Customer:")
        credit = extract_value(block, "Credit:")
        description = extract_value(block, "Description:")

        fee_val = extract_value(block, "Fee:")
        fee_match = re.search(r"([0-9]{1,3}[,.]?[0-9]{0,2})", fee_val)
        fee_clean = float(fee_match.group(1).replace(",", ".")) if fee_match else 0.0

        share_pct = extract_value(block, "Your share (%):")
        share_val = extract_value(block, "Your share (€):")

        try:
            share_pct_float = float(share_pct)
        except:
            share_pct_float = 0.0

        try:
            share_val_float = float(share_val.replace(",", "."))
        except:
            share_val_float = round((fee_clean * share_pct_float / 100), 2)

        media_link = f"https://www.nurphoto.com/photo/{media_number}"
        thumbnail = f"<a href='{media_link}' target='_blank'><img src='https://www.nurphoto.com/photo/{media_number}/picture/photo' width='100'/></a>"

        record = {
            "Media Number": media_number,
            "Filename": filename,
            "Original Filename": original_filename,
            "Customer": customer,
            "Credit": credit,
            "Description": description,
            "Fee": fee_clean,
            "Currency": "EUR",
            "Your Share (%)": share_pct_float,
            "Your Share": share_val_float,
            "Agency": "NurPhoto",
            "Media Link": media_link,
            "Thumbnail": thumbnail,
            "Slug?": False
        }

        records.append(record)

    df = pd.DataFrame(records)
    if "Thumbnail" in df.columns:
        thumb = df.pop("Thumbnail")
        df.insert(0, "Thumbnail", thumb)

    return df
