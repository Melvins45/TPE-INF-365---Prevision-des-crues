from pypdf import PdfReader
import os

pdf_files = [
    "TPE INF 365 - GROUPE 24 - Prévision des crues - Cahier de charges.pdf",
    "TPE INF 365 - GROUPE 24 - Prévision des crues - Etat d'avancement.pdf"
]

for pdf_file in pdf_files:
    if os.path.exists(pdf_file):
        print(f"--- Reading {pdf_file} ---")
        try:
            reader = PdfReader(pdf_file)
            # Read first few pages which usually contain the title and group members
            for i in range(min(3, len(reader.pages))):
                page = reader.pages[i]
                text = page.extract_text()
                print(f"Page {i+1}:")
                print(text)
                print("-" * 20)
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")
    else:
        print(f"File not found: {pdf_file}")
