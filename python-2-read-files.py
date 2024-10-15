using weasy
=================================================

import os
import argparse
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from weasyprint import HTML

def generate_html_content(file_path, file_extension):
    """
    Convert the content of a supported file to HTML with syntax highlighting if applicable.
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Handle unsupported file types like .info (treat as plain text)
    if file_extension == '.info':
        return f"<pre>{content}</pre>"

    # Add syntax highlighting for supported code files using Pygments
    try:
        lexer = get_lexer_by_name(file_extension.strip('.'))
        formatter = HtmlFormatter(style='colorful', full=True, noclasses=True)
        return highlight(content, lexer, formatter)
    except Exception as e:
        # If no lexer is found, treat the file as plain text
        print(f"No lexer found for {file_extension}, treating as plain text.")
        return f"<pre>{content}</pre>"

def process_files_in_folder(root_folder):
    """
    Traverse nested folders, process text files within them, and generate HTML content.
    Skip image files like .png, .jpg, .jpeg.
    """
    html_content = "<html><body>"
    for root, dirs, files in os.walk(root_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_extension = os.path.splitext(file_name)[1].lower()

            # Skip image files like .png, .jpg, .jpeg
            if file_extension in ['.png', '.jpg', '.jpeg']:
                print(f"Skipping image file: {file_name}")
                continue

            # Process only text-based files
            if is_text_file(file_extension):
                html_content += f"<h2>{file_name}</h2>"
                html_content += generate_html_content(file_path, file_extension)
    
    html_content += "</body></html>"
    return html_content

def is_text_file(extension):
    """
    Checks if the file is a text-based file.
    """
    return extension in ['.xml', '.html', '.css', '.js', '.javascript', '.info']

def create_pdf_from_folder(folder_path, output_pdf):
    """
    Traverse the folder, convert files to HTML, and create a single PDF using WeasyPrint.
    """
    html_content = process_files_in_folder(folder_path)

    # Convert the HTML content to PDF using WeasyPrint
    HTML(string=html_content).write_pdf(output_pdf)
    print(f"PDF created successfully: {output_pdf}")

def parse_arguments():
    """
    Parse command-line arguments to get the folder path and output PDF file name.
    """
    parser = argparse.ArgumentParser(description="Convert files in a folder to a single PDF using WeasyPrint.")
    parser.add_argument('--folder-path', type=str, required=True, help='Path to the folder containing the files.')
    parser.add_argument('--output-pdf', type=str, required=True, help='Name of the output PDF file.')

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Pass the folder path and output PDF to the function
    create_pdf_from_folder(args.folder_path, args.output_pdf)




    
------------------------------------------
import os
import argparse
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from weasyprint import HTML

def generate_html_content(file_path, file_extension):
    """
    Convert the content of a supported file to HTML with syntax highlighting if applicable.
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Add syntax highlighting for code files using Pygments
    if file_extension in ['.xml', '.html', '.css', '.js', '.javascript', '.info']:
        lexer = get_lexer_by_name(file_extension.strip('.'))
        formatter = HtmlFormatter(style='colorful', full=True, noclasses=True)
        return highlight(content, lexer, formatter)
    
    # For plain text, return the content wrapped in a <pre> tag
    return f"<pre>{content}</pre>"

def process_files_in_folder(root_folder):
    """
    Traverse nested folders, process text files within them, and generate HTML content.
    Skip image files like .png, .jpg, .jpeg.
    """
    html_content = "<html><body>"
    for root, dirs, files in os.walk(root_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_extension = os.path.splitext(file_name)[1].lower()

            # Skip image files like .png, .jpg, .jpeg
            if file_extension in ['.png', '.jpg', '.jpeg']:
                print(f"Skipping image file: {file_name}")
                continue

            # Process only text-based files
            if is_text_file(file_extension):
                html_content += f"<h2>{file_name}</h2>"
                html_content += generate_html_content(file_path, file_extension)
    
    html_content += "</body></html>"
    return html_content

def is_text_file(extension):
    """
    Checks if the file is a text-based file.
    """
    return extension in ['.xml', '.html', '.css', '.js', '.javascript', '.info']

def create_pdf_from_folder(folder_path, output_pdf):
    """
    Traverse the folder, convert files to HTML, and create a single PDF using WeasyPrint.
    """
    html_content = process_files_in_folder(folder_path)

    # Convert the HTML content to PDF using WeasyPrint
    HTML(string=html_content).write_pdf(output_pdf)
    print(f"PDF created successfully: {output_pdf}")

def parse_arguments():
    """
    Parse command-line arguments to get the folder path and output PDF file name.
    """
    parser = argparse.ArgumentParser(description="Convert files in a folder to a single PDF using WeasyPrint.")
    parser.add_argument('--folder-path', type=str, required=True, help='Path to the folder containing the files.')
    parser.add_argument('--output-pdf', type=str, required=True, help='Name of the output PDF file.')

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Pass the folder path and output PDF to the function
    create_pdf_from_folder(args.folder_path, args.output_pdf)

=====================================================================
import os
from PIL import Image
from fpdf import FPDF

class PrettyPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Test Output Collation', ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

def process_image(pdf, file_path):
    """
    Process image files from a file path and verify they are valid.
    Adds the image to the PDF.
    """
    try:
        # Open the image directly from file
        img = Image.open(file_path)
        img.verify()  # Verify the image is valid

        # Add a new page and embed the image into the PDF
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        file_name = os.path.basename(file_path)
        pdf.cell(0, 10, f'Image: {file_name}', ln=True)
        pdf.image(file_path, x=10, y=30, w=pdf.w - 20)
        print(f"Successfully loaded and verified image: {file_path}")
    except PIL.UnidentifiedImageError:
        print(f"Cannot identify image file: {file_path}")
    except Exception as e:
        print(f"Error loading image {file_path}: {str(e)}")

def process_image_in_nested_folder(pdf, root_folder):
    """
    Traverse nested folders and process image files within them.
    """
    for root, dirs, files in os.walk(root_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Only process image files
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                process_image(pdf, file_path)

def create_pdf_from_folder(folder_path, output_pdf):
    """
    Traverse the folder, process files, and create a single PDF.
    """
    pdf = PrettyPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Traverse the folder and all subfolders
    process_image_in_nested_folder(pdf, folder_path)

    # Save the resulting PDF
    pdf.output(output_pdf)
    print(f"PDF created successfully: {output_pdf}")

if __name__ == "__main__":
    folder_path = "path_to_your_nested_folder"
    output_pdf = "output_pdf_file.pdf"
    create_pdf_from_folder(folder_path, output_pdf)



=============================================
import os
import io
import argparse
from PIL import Image
from fpdf import FPDF
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from weasyprint import HTML

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

    # Handle HTML files with WeasyPrint
    if file_extension == '.html':
        # Convert HTML content to PDF using WeasyPrint
        output_pdf_file = f"{file_name}.pdf"
        HTML(string=content).write_pdf(output_pdf_file)
        
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f'Embedded HTML File: {file_name}', ln=True)
        pdf.ln(10)
        pdf.image(output_pdf_file, x=10, y=20, w=pdf.w - 20)  # Embed as image (or merge PDFs)
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

def process_image(pdf, file_path):
    """
    Process image files from a file path and verify they are valid.
    Adds the image to the PDF.
    """
    try:
        with open(file_path, 'rb') as image_file:
            img = Image.open(image_file)
            img.verify()  # Verify the image is valid
            
            # Add a new page and embed the image into the PDF
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            file_name = os.path.basename(file_path)
            pdf.cell(0, 10, f'Image: {file_name}', ln=True)
            pdf.image(file_path, x=10, y=30, w=pdf.w - 20)
            print(f"Successfully loaded and verified image: {file_path}")
    except PIL.UnidentifiedImageError:
        print(f"Cannot identify image file: {file_path}")
    except Exception as e:
        print(f"Error loading image {file_path}: {str(e)}")

def process_image_in_nested_folder(pdf, root_folder):
    """
    Traverse nested folders and process image files within them.
    """
    for root, dirs, files in os.walk(root_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Only process image files
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                process_image(pdf, file_path)
            elif is_text_file(os.path.splitext(file_name)[1].lower()):
                add_text_file_to_pdf(pdf, file_path, os.path.splitext(file_name)[1].lower())

def is_text_file(extension):
    """
    Checks if the file is a text-based file.
    """
    return extension in ['.xml', '.html', '.css', '.js', '.javascript', '.info']

def create_pdf_from_folder(folder_path, output_pdf):
    """
    Traverse the folder, process files, and create a single PDF.
    """
    pdf = PrettyPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Traverse the folder and all subfolders
    process_image_in_nested_folder(pdf, folder_path)

    # Save the resulting PDF
    pdf.output(output_pdf)
    print(f"PDF created successfully: {output_pdf}")

if __name__ == "__main__":
    # Argument parser to get folder path and output PDF file name
    parser = argparse.ArgumentParser(description="Create a PDF from folder contents.")
    parser.add_argument('--folder-path', required=True, help="Path to the folder containing files.")
    parser.add_argument('--output', required=True, help="Output PDF file name.")

    args = parser.parse_args()

    # Call the function to create a PDF from the folder
    create_pdf_from_folder(args.folder_path, args.output)


=================================================
import os
import argparse
from fpdf import FPDF
from weasyprint import HTML
from PIL import Image
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

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

    # Handle HTML files with WeasyPrint
    if file_extension == '.html':
        pdf_file_name = f"{file_name}.pdf"
        HTML(string=content).write_pdf(pdf_file_name)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f'Embedded HTML File: {file_name}', ln=True)
        pdf.ln(10)
        pdf.image(pdf_file_name, x=10, y=20, w=pdf.w - 20)  # Embed as image (or merge PDFs)
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

if __name__ == "__main__":
    # Argument parser to get folder path and output PDF file name
    parser = argparse.ArgumentParser(description="Create a PDF from folder contents.")
    parser.add_argument('--folder-path', required=True, help="Path to the folder containing files.")
    parser.add_argument('--output', required=True, help="Output PDF file name.")

    args = parser.parse_args()

    # Call the function to create a PDF from the folder
    create_pdf_from_folder(args.folder_path, args.output)



======================================
import os
import argparse
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

if __name__ == "__main__":
    # Argument parser to get folder path and output PDF file name
    parser = argparse.ArgumentParser(description="Create a PDF from folder contents.")
    parser.add_argument('--folder-path', required=True, help="Path to the folder containing files.")
    parser.add_argument('--output', required=True, help="Output PDF file name.")

    args = parser.parse_args()

    # Call the function to create a PDF from the folder
    create_pdf_from_folder(args.folder_path, args.output)



========================================================
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
