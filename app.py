import numpy as np
import streamlit as st
from pygments.formatters import img

from scripts.pdf_extractor import  extract_text_from_pdf, extract_text_from_scanned_pdf, extract_table_from_pdf
import os
from scripts.db import save_extracted_data, init_db

init_db()
st.set_page_config(page_title="AI PDF Extractor", layout="wide")

st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #007bff; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("📄 AI-Powered PDF Data Extraction")
st.write("Upload a PDF file to extract text, tables, and images using AI.")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    pdf_path = f"temp_{uploaded_file.name}"

    # Save the uploaded file temporarily
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract Data
    text = extract_text_from_pdf(pdf_path)
    scanned_text = extract_text_from_scanned_pdf(pdf_path)
    tables = extract_table_from_pdf(pdf_path)

    # Display Results
    st.subheader("Extracted Text:")
    st.text_area("Normal PDF Text:", text, height=200)

    st.subheader("Extracted Tables:")
    st.table(tables)
    st.subheader("Extracted Images:")

    if isinstance(img, str) and img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        st.image(img)
    elif isinstance(img, np.ndarray):
        st.image(img, channels="BGR")
    elif isinstance(img, list):
        for image in img:
            if isinstance(image, str) and image.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                st.image(image)
            elif isinstance(image, np.ndarray):
                st.image(image, channels="BGR")
            else:
                st.warning("Invalid image detected.")
    else:
        st.warning("No valid image found!")
    save_extracted_data(uploaded_file.name, text, tables)
    st.success("Data saved successfully! ✅")

    if scanned_text:
        st.text_area("Scanned PDF Text (OCR):", scanned_text, height=200)

    st.subheader("Extracted Tables:")
    for table in tables:
        st.write(table)

