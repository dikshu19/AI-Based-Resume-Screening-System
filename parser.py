import PyPDF2
import docx

def extract_text_from_pdf(pdf_file):
    text = ""
    
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page in pdf_reader.pages:
        text += page.extract_text()

    return text


def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text