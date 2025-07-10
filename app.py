import streamlit as st
import io

from utils.parsers import parse_pdf, detect_agency_from_text

st.set_page_config(page_title="Sales Report Parser", layout="wide")

st.title("Sales Report Parser")
st.write("Upload your Getty/iStock, Nurphoto, or EditorialFootage sales report file (CSV, TXT, MHTML supported).")

uploaded_file = st.file_uploader(
    "Upload sales report file (CSV, TXT, MHTML)", 
    type=["csv", "txt", "mhtml"]
)

df = None
parsed_agency = None

if uploaded_file is not None:
    # Attempt to auto-detect agency from the file name and initial content
    filename = uploaded_file.name
    filename_lower = filename.lower()

    # Read a small sample for agency detection
    sample_bytes = uploaded_file.read(2048)
    uploaded_file.seek(0)
    try:
        sample_text = sample_bytes.decode("utf-8", errors="ignore")
    except Exception:
        sample_text = ""

    # Try to auto-detect agency from filename and sample content
    agency = detect_agency_from_text(filename + " " + sample_text)
    if agency == "Unknown":
        st.warning("Could not auto-detect agency. Please check your file or contact support.")

    # Use full file bytes for parsing (reset file pointer)
    file_bytes = uploaded_file.read()
    uploaded_file.seek(0)

    try:
        df, parsed_agency = parse_pdf(
            file_bytes,
            agency=agency,
            with_keywords=False,
            filename=filename
        )

        if df is not None and not df.empty:
            st.success(f"Parsed {parsed_agency} report with {len(df)} rows.")

            st.dataframe(df.head(100), use_container_width=True)

            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Parsed CSV",
                data=csv,
                file_name=f"parsed_{parsed_agency.lower()}_sales_report.csv",
                mime="text/csv"
            )

            # Show thumbnails if present
            if "Thumbnail" in df.columns:
                st.write("Thumbnails Preview (first 10 rows):")
                for thumbnail_html in df["Thumbnail"].head(10):
                    st.markdown(thumbnail_html, unsafe_allow_html=True)

        else:
            st.warning("No data found in the uploaded file.")

    except Exception as e:
        st.error(f"Error parsing file: {str(e)}")

else:
    st.info("Please upload your Getty/iStock, Nurphoto, or EditorialFootage sales report file (CSV, TXT, or MHTML).")
