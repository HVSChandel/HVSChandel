import PyPDF2

def pdf_to_text(input_pdf, output_text):
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        with open(output_text, 'w') as text_file:
            for page_number in range(num_pages):
                page = pdf_reader.pages[page_number]
                text_file.write(page.extract_text())

if __name__ == "__main__":
    input_pdf_file = "/home/harsh/HVSChandel/Minor Projects/Chat_Bot/bd-chaurasias-handbook-of-general-anatomy.pdf"
    output_text_file = "Medical_data.txt"

    pdf_to_text(input_pdf_file, output_text_file)

