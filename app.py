import streamlit as st
import pandas as pd
from utils.parsers import parse_pdf, detect_agency_from_text

st.set_page_config(page_title="Sales Report Extractor", layout="wide")
st.title("📊 Sales Report Parser & Formatter")

include_keywords = st.checkbox("🔑 Fetch Keywords from iStock", value=False)

uploaded_file = st.file_uploader("Upload a Sales Report (PDF, CSV, or MHTML)", type=["pdf", "csv", "mhtml"])

if uploaded_file:
    pdf_bytes = uploaded_file.read()
    file_type = uploaded_file.type

    with st.spinner("Detecting agency and processing file..."):
        if file_type == "text/csv":
            agency = "Getty/iStock"
        elif uploaded_file.name.lower().endswith(".mhtml"):
            agency = "NurPhoto"
        else:
            agency = detect_agency_from_text(pdf_bytes)

        df, parsed_agency = parse_pdf(pdf_bytes, agency, with_keywords=include_keywords)

        if df is not None and not df.empty:
            st.success(f"Parsed {parsed_agency} report with {len(df)} records")

            if "Thumbnail" in df.columns:
                st.write("\n**Thumbnail Preview Table**")
                st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{parsed_agency}_report_parsed.csv",
                mime="text/csv"
            )
        else:
            st.warning("No usable data found. Please verify the file format.")
