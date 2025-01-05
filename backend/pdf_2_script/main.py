"""
Main module to convert PDF to podcast.
"""
import os
from .pdf_2_png import convert_pdf_to_png
from .extract_text import extract_text_from_images_in_folder
from .script_gen import create_script
from .GoogleTTS.tts import create_podcast


def main(pdf_path, output_folder, pdf_name):
    """
    Main function to convert a PDF to a podcast.
    
    Args:
        pdf_path (str): The path to the PDF file.
        output_folder (str): The base directory where the output images will be saved.
        pdf_name (str): The name of the PDF file (used for naming the output folder and file).
    """
    print("Converting PDF to PNG images...")
    convert_pdf_to_png(pdf_path, output_folder)

    print("Extracting text from images...")
    extract_text_from_images_in_folder(
        output_folder,
        'TEMPORARY_FILES_FOLDER/text_output_folder/extracted_text',
        pdf_name)

    print("Creating script for podcast from text...")
    create_script(pdf_name)

    print("Creating podcast from script...")
    create_podcast(pdf_name)

if __name__ == "__main__":
    PDF_PATH = 'pdf_2_script/pdfs/EdPsy2009.pdf'
    PDF_NAME = os.path.splitext(os.path.basename(PDF_PATH))[0]
    OUTPUT_FOLDER = 'pdf_2_script/output_images'
    main(PDF_PATH, OUTPUT_FOLDER, PDF_NAME)
