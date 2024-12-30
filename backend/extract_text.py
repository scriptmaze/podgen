import os
import boto3

textract_client = boto3.client('textract', region_name='us-east-1')

def extract_text_from_image(image_path, page_num, output_folder, pdf_name):
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})

    extracted_text = ""
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text += item['Text'] + '\n'

    pdf_output_folder = os.path.join(output_folder, pdf_name)
    if not os.path.exists(pdf_output_folder):
        os.makedirs(pdf_output_folder)

    text_output_path = os.path.join(pdf_output_folder, f"page_{page_num}.txt")
    with open(text_output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(extracted_text)

    print(f"Extracted text saved to {text_output_path}")

def extract_text_from_images_in_folder(input_folder, output_folder, pdf_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        if os.path.basename(root) == pdf_name:
            for image_name in files:
                if image_name.endswith('.png'):  # Only process PNG images
                    image_path = os.path.join(root, image_name)

                    page_num = int(image_name.split('_')[1].split('.')[0])

                    extract_text_from_image(image_path, page_num, output_folder, pdf_name)
