"""
Module to convert PDF pages to PNG images.
"""
import os
import fitz

def create_output_folder(pdf_path, base_output_folder):
    """
    Create an output folder for the converted PNG files.
    
    Args:
        pdf_path (str): The path to the PDF file.
        base_output_folder (str): The base directory where the output folder will be created.
    
    Returns:
        str: The path to the created output folder.
    """
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(base_output_folder, pdf_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def convert_pdf_to_png(pdf_path, base_output_folder):
    """
    Convert each page of a PDF file to a PNG image.
    
    Args:
        pdf_path (str): The path to the PDF file.
        base_output_folder (str): The base directory where the output images will be saved.
    """
    try:
        output_folder = create_output_folder(pdf_path, base_output_folder)
        document = fitz.open(pdf_path)
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            pix = page.get_pixmap(dpi=300)
            output_image_path = f"{output_folder}/page_{page_num + 1}.png"
            pix.save(output_image_path)
            print(f"Saved {output_image_path}")

    except Exception as e:
        print(f"Error in convert_pdf_to_png: {e}")
        raise  # Re-raise the exception to propagate it
