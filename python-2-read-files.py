import os
from fpdf import FPDF
from PIL import Image
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import pdfkit

class PrettyPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Test Output Collation', ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

def add_text_file_to_pdf(pdf, file_path, file_extension):
    """
    Reads a text-based file and adds its content to the PDF.
    Supports .xml, .html, .css, .js, .javascript, .info files.
    """
    pdf.add_page()
    
    # Add file title as header
    file_name = os.path.basename(file_path)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f'File: {file_name}', ln=True)

    # Read the file content
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Handle HTML files with pdfkit (optional)
    if file_extension == '.html':
        html_pdf = f"{file_name}.pdf"
        pdfkit.from_file(file_path, html_pdf)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f'Embedded HTML File: {file_name}', ln=True)
        pdf.ln(10)
        pdf.image(html_pdf, x=10, y=20, w=pdf.w - 20)  # Embed as image (or merge PDFs)
        return

    # Syntax highlighting for code files
    if file_extension in ['.js', '.css', '.xml', '.javascript']:
        lexer = get_lexer_by_name(file_extension.lstrip('.'), stripall=True)
        formatter = HtmlFormatter(style='colorful', full=True)
        highlighted_code = highlight(content, lexer, formatter)

        # Add formatted code
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, highlighted_code)
    else:
        # Add normal text files
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)

def add_image_to_pdf(pdf, image_path):
    """
    Adds an image (.png) to the PDF with proper formatting.
    """
    pdf.add_page()
    file_name = os.path.basename(image_path)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f'Image: {file_name}', ln=True)
    pdf.image(image_path, x=10, y=30, w=pdf.w - 20)

def is_text_file(extension):
    """
    Checks if the file is a text-based file.
    """
    return extension in ['.xml', '.html', '.css', '.js', '.javascript', '.info']

def is_image_file(extension):
    """
    Checks if the file is an image file.
    """
    return extension in ['.png']

def create_pdf_from_folder(folder_path, output_pdf):
    """
    Traverse the folder, process files, and create a single PDF.
    """
    pdf = PrettyPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Traverse the folder and all subfolders
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_extension = os.path.splitext(file_name)[1].lower()

            # Add text-based files to the PDF
            if is_text_file(file_extension):
                add_text_file_to_pdf(pdf, file_path, file_extension)
                print(f"Added text file {file_path} to PDF.")
            
            # Add image files to the PDF
            elif is_image_file(file_extension):
                add_image_to_pdf(pdf, file_path)
                print(f"Added image {file_path} to PDF.")
            
            else:
                print(f"Skipped unsupported file type: {file_name}")

    # Save the resulting PDF
    pdf.output(output_pdf)
    print(f"PDF created successfully: {output_pdf}")

# Example usage
folder_path = 'path_to_your_jest_output_folder'  # Replace with the path to your folder
output_pdf = 'test_results_pretty.pdf'  # Output PDF file name
create_pdf_from_folder(folder_path, output_pdf)

=============================================
import os
import argparse
from fpdf import FPDF
from PIL import Image

def add_text_file_to_pdf(pdf, file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)

def add_image_to_pdf(pdf, image_path):
    pdf.add_page()
    pdf.image(image_path, x=10, y=10, w=pdf.w - 20)

def is_text_file(extension):
    return extension in ['.xml', '.html', '.css', '.js', '.javascript', '.info']

def is_image_file(extension):
    return extension in ['.png']

def create_pdf_from_folder(folder_path, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_extension = os.path.splitext(file_name)[1].lower()

            if is_text_file(file_extension):
                add_text_file_to_pdf(pdf, file_path)
                print(f"Added text file {file_path} to PDF.")
            elif is_image_file(file_extension):
                add_image_to_pdf(pdf, file_path)
                print(f"Added image {file_path} to PDF.")
            else:
                print(f"Skipped unsupported file type: {file_name}")

    pdf.output(output_pdf)
    print(f"PDF created successfully: {output_pdf}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a PDF from folder contents.")
    parser.add_argument('--folder-path', required=True, help="Path to the folder containing files.")
    parser.add_argument('--output', required=True, help="Output PDF file name.")

    args = parser.parse_args()
    create_pdf_from_folder(args.folder_path, args.output)



===========================================
import os
from fpdf import FPDF
from PIL import Image

def add_text_file_to_pdf(pdf, file_path):
    """
    Reads a text-based file and adds its content to the PDF.
    Supports .xml, .html, .css, .js, .javascript, .info files.
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Add a new page for each text file
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)

def add_image_to_pdf(pdf, image_path):
    """
    Adds an image (.png) to the PDF.
    """
    pdf.add_page()
    # Automatically resize image to fit the page
    pdf.image(image_path, x=10, y=10, w=pdf.w - 20)

def is_text_file(extension):
    """
    Checks if the file is a text-based file.
    """
    return extension in ['.xml', '.html', '.css', '.js', '.javascript', '.info']

def is_image_file(extension):
    """
    Checks if the file is an image file.
    """
    return extension in ['.png']

def create_pdf_from_folder(folder_path, output_pdf):
    """
    Traverse the folder, process files, and create a single PDF.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Traverse the folder and all subfolders
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_extension = os.path.splitext(file_name)[1].lower()

            # Add text-based files to the PDF
            if is_text_file(file_extension):
                add_text_file_to_pdf(pdf, file_path)
                print(f"Added text file {file_path} to PDF.")
            
            # Add image files to the PDF
            elif is_image_file(file_extension):
                add_image_to_pdf(pdf, file_path)
                print(f"Added image {file_path} to PDF.")
            
            else:
                print(f"Skipped unsupported file type: {file_name}")

    # Save the resulting PDF
    pdf.output(output_pdf)
    print(f"PDF created successfully: {output_pdf}")

# Example usage
folder_path = 'path_to_your_jest_output_folder