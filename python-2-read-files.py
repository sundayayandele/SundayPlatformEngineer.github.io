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
