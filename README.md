# 📊 Sales Report Parser

A lightweight Streamlit app that processes PDF sales reports and outputs cleaned CSVs for Google Sheets ingestion.

## Features

- Upload and parse royalty statements
- Normalize across agencies
- Enrich data with media links, thumbnail previews, internal slug detection
- Export to CSV

## To Run Locally

```bash
python3 -m venv venv
source venv/bin/activate        # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
```
