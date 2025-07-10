# app.py

import streamlit as st
import pandas as pd
from utils.parsers import parse_pdf

st.set_page_config(page_title="Sales Report Extractor", layout="wide")
st.title("📊 Sales Report Parser & Formatter")

# Upload form
uploaded_file = st.file_uploader("Upload a PDF Sales Report", type="pdf")

# Select agency from dropdown
agency = st.selectbox("Select Agency", ["NurPhoto", "SIPA USA", "Getty/iStock"])

if uploaded_file:
    with st.spinner("Processing..."):
        pdf_bytes = uploaded_file.read()
        df, parsed_agency = parse_pdf(pdf_bytes, agency)

        if df is not None:
            st.success(f"Parsed {parsed_agency} report with {len(df)} records")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{parsed_agency}_report_parsed.csv",
                mime="text/csv"
            )
        else:
            st.error("Could not parse this file. Is it a supported format?")
