from PyPDF2 import PdfReader
import docx 
import textract
import win32com.client
import subprocess
import pythoncom
import os

def extract_text_from_pdf(file_path):
    pdf_document = PdfReader(file_path)
    text = ""
    for page in pdf_document.pages:
        text += page.extract_text()
    print(text)    
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    print(text)
    return text


def extract_text_from_doc(file_path):
    try:
        # Using textract to extract text from .doc file
        text = textract.process(file_path)
        print(text)
        # textract returns a byte string, so we need to decode it
        return text.decode('utf-8')
    except Exception as e:
        print(f"Error extracting text from .doc file: {e}")
        return None
    
# def extract_text_from_doc(file_path):
#     word = win32com.client.Dispatch("Word.Application")
#     doc = word.Document.Open(file_path)
#     doc_content = doc.Content.Text
#     doc.Close()
#     word.Quit()
#     print(doc_content)
#     return doc_content

# def extract_text_from_doc(file_path):
#     process = subprocess.Popen(['antiword', file_path], stdout=subprocess.PIPE)
#     output, _ = process.communicate()
#     print(output)
#     return output.decode('utf-8')


def extract_text_from_doc(file_path):
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Initialize COM library
    pythoncom.CoInitialize()

    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        
        # Try opening the document
        try:
            doc = word.Documents.Open(file_path)
        except Exception as e:
            raise Exception(f"Failed to open document: {e}")

        # Extract text
        try:
            text = doc.Content.Text
        except Exception as e:
            raise Exception(f"Failed to extract text: {e}")
        finally:
            doc.Close()

        word.Quit()
        return text

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Uninitialize COM library
        pythoncom.CoUninitialize()
