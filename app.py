import streamlit as st
import io

from utils.getty_statement_parser import parse_getty_statement_csv
from utils.getty_csv_parser import parse_getty_csv  # Keep for legacy support
# from utils.parsers import detect_agency_from_text  # Uncomment if needed for agency auto-detection

st.set_page_config(page_title="Sales Report Parser", layout="wide")

st.title("Sales Report Parser")
st.write("Upload your Getty/iStock statement or legacy CSV report.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv", "txt"])
file_type = None
df = None
parsed_agency = None

if uploaded_file is not None:
    # Detect file type - here we use filename heuristic, adapt if needed!
    filename = uploaded_file.name.lower()
    if "statement" in filename or "dm-" in filename:
        file_type = "statement"
    else:
        file_type = "getty_csv"

    try:
        if file_type == "statement":
            df, parsed_agency = parse_getty_statement_csv(uploaded_file)
        else:
            # For legacy CSV format
            df, parsed_agency = parse_getty_csv(uploaded_file)

        if df is not None and not df.empty:
            st.success(f"Parsed {parsed_agency} report with {len(df)} rows.")

            # Display preview
            st.dataframe(df.head(100), use_container_width=True)

            # Download button (CSV)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Parsed CSV",
                data=csv,
                file_name="parsed_sales_report.csv",
                mime="text/csv"
            )

            # Optionally show thumbnails
            if "Thumbnail" in df.columns:
                st.write("Thumbnails Preview (first 10 rows):")
                for thumbnail_html in df["Thumbnail"].head(10):
                    st.markdown(thumbnail_html, unsafe_allow_html=True)

        else:
            st.warning("No data found in the uploaded file.")

    except Exception as e:
        st.error(f"Error parsing file: {str(e)}")

else:
    st.info("Please upload your Getty/iStock statement CSV or legacy report.")
