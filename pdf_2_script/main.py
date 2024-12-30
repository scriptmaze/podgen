from pdf_2_png import convert_pdf_to_png
from extract_text import extract_text_from_images_in_folder
from script_gen import create_script
import os

def main(pdf_path, output_folder, pdf_name):
    print("Converting PDF to PNG images...")
    convert_pdf_to_png(pdf_path, output_folder)

    print("Extracting text from images...")
    extract_text_from_images_in_folder(output_folder, 'pdf_2_script/extracted_text', pdf_name)

    print("Creating script for podcast from text...")
    create_script(pdf_name)


if __name__ == "__main__":
    pdf_path = 'pdf_2_script/pdfs/EdPsy2009.pdf'
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = 'pdf_2_script/output_images'
    main(pdf_path, output_folder, pdf_name)

