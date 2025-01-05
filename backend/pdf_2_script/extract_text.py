"""
Module to extract text from images using AWS Textract.
"""
import os
import boto3

textract_client = boto3.client('textract', region_name='us-east-1')

def extract_text_from_image(image_path, output_folder, pdf_name):
    """
    Extract text from a single image using AWS Textract and save it to a text file.
    
    Args:
        image_path (str): The path to the image file.
        output_folder (str): The base directory where the output text file will be saved.
        pdf_name (str): The name of the PDF file (used for naming the output folder and file).
    """
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})

    extracted_text = ""
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text += item['Text'] + '\n'

    # Ensure the output folder exists
    pdf_output_folder = os.path.join(output_folder, pdf_name)
    if not os.path.exists(pdf_output_folder):
        os.makedirs(pdf_output_folder)

    # Combine all extracted text into a single file
    text_output_path = os.path.join(pdf_output_folder, f"{pdf_name}.txt")
    with open(text_output_path, 'a', encoding='utf-8') as text_file:
        text_file.write(extracted_text)

    print(f"Extracted text appended to {text_output_path}")

def extract_text_from_images_in_folder(input_folder, output_folder, pdf_name):
    """
    Extract text from all images in a folder using AWS Textract and save it to a text file.
    
    Args:
        input_folder (str): The directory containing the image files.
        output_folder (str): The base directory where the output text file will be saved.
        pdf_name (str): The name of the PDF file (used for naming the output folder and file).
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over the files in the input folder
    for root, dirs, files in os.walk(input_folder):
        if os.path.basename(root) == pdf_name:
            for image_name in files:
                if image_name.endswith('.png'):  # Only process PNG images
                    image_path = os.path.join(root, image_name)

                    extract_text_from_image(image_path, output_folder, pdf_name)
