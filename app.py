import streamlit as st
import pandas as pd
from scraper import run_scraper
import io


st.set_page_config(
    page_title="THD Product Scraper",
    layout="wide"
)


st.title(
    "🏠 THD Product Scraper"
)


st.write(
    "Upload THD URL Excel file to collect product information and specifications."
)


uploaded_file = st.file_uploader(
    "Upload Excel",
    type=["xlsx"]
)


if uploaded_file:


    df = pd.read_excel(
        uploaded_file
    )


    st.subheader(
        "Uploaded Products"
    )

    st.dataframe(df)


    if st.button(
        "Start Scraping"
    ):


        with st.spinner(
            "Scraping THD data..."
        ):


            output = run_scraper(
                df
            )


            st.success(
                "Completed!"
            )


            st.download_button(
                label="Download Excel",
                data=output,
                file_name="THD_Product_Data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
