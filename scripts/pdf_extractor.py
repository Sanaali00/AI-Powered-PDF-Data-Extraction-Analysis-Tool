import fitz
import pdfplumber
import pytesseract
import io
from PIL import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(pdf_path):
    """Extracts text from normal PDFs."""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()
def extract_table_from_pdf(pdf_path):
    """Extracts table from normal PDFs."""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                tables.append(table)
    return tables

def extract_text_from_scanned_pdf(pdf_path):
    """Extracts text from scanned PDFs."""
    doc = fitz.open(pdf_path)
    extracted_text = ""

    for page_num in range(len(doc)):
        img = doc[page_num].get_pixmap()
        img_bytes = img.tobytes("ppm")
        img_pil = Image.open(io.BytesIO(img_bytes))
        text = pytesseract.image_to_string(img_pil)
        extracted_text += text + "\n"

    return extracted_text.strip()

