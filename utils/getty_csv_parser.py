import pandas as pd
import io

def parse_getty_csv(csv_file, with_keywords=False):
    # Dummy implementation – replace with your original!
    content = csv_file.read()
    if isinstance(content, bytes):
        text = content.decode("utf-8")
    else:
        text = content
    df = pd.read_csv(io.StringIO(text))
    return df, "Getty/iStock"
