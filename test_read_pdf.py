from pypdf import PdfReader
import os

pdf_files = [
    "TPE INF 365 - GROUPE 24 - Prévision des crues - Cahier de charges.pdf",
    "TPE INF 365 - GROUPE 24 - Prévision des crues - Etat d'avancement.pdf"
]

for pdf_file in pdf_files:
    print(f"Checking: {pdf_file}")
    if os.path.exists(pdf_file):
        print(f"--- Reading {pdf_file} ---")
        try:
            reader = PdfReader(pdf_file)
            print(f"Total pages: {len(reader.pages)}")
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    print(f"Page {i+1} content found.")
                    print(text[:1000]) # Print first 1000 chars of each page
                else:
                    print(f"Page {i+1} has no text.")
                print("-" * 20)
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")
    else:
        print(f"File not found: {pdf_file}")
