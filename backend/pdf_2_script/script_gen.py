import boto3
import json
import os
from django.conf import settings  # To get the base project path

# Initialize the Bedrock client
bedrock = boto3.client(service_name="bedrock-runtime")
TEMP_FILES_PATH = os.path.join(settings.BASE_DIR, 'TEMPORARY_FILES_FOLDER')

# Ensure necessary directories exist
def ensure_directories_exist(base_path, subfolders):
    for subfolder in subfolders:
        full_path = os.path.join(base_path, subfolder)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Created directory: {full_path}")

# Read file utility
def read_file(file_path):
    try:
        print(f"Reading file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"File read successfully: {file_path}")
            return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        raise

# Send prompt to Bedrock API
def send_prompt(pdf_name):
    try:
        # Construct the file path for the extracted text
        file_path = os.path.join(
            TEMP_FILES_PATH, 
            'text_output_folder', 
            'extracted_text', 
            pdf_name, 
            f"{pdf_name}.txt"
        )
        print(f"Constructed file path: {file_path}")

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read the file content
        file_content = read_file(file_path)

        # Create the request body
        body = json.dumps({
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "user",
                    "content": f"""
    I have given you data in a txt file that represents information in a textbook. I need you to identify the key concepts, the sections, etc. and create a conversational script of 2 people talking about the subject. The idea is that if theres a lot of different subjects, you could alternate the person that explains and the one that is learning. The one learning could also ask questions, or it could make them think about the next subject, which could create a segway into the next subject. You don't need to always have it so that the 2 people will have turns being the "teacher".
    It is important that you don't mention in the text the prompt I gave you. So don't say like "Here are the key components..." etc. It needs to feel like a real podcast.
    It is also important to not skip lines if the same person keeps talking. If you want to use list items, like 1. 2. 3., use First, Second, etc. or other similar words.
    Also, dont abuse of conversational key points like, wow that's interesting! Include them, but keep in mind that a podcast should be one person for example talking 2-3 phrases or more, and the other replying, etc.
    
    The structure of the script has to be the following (consider only the structure, like the [1], [2], not the Hi John or the text after) :
    [1] Hello!
    [2] Hi John.
    [1] Today I learned about mathematics.
    [2] That is cool! Tell me more about it.

    Also, no need to put 2 skip lines after a line. You can put one line after the other.

    Now, please process the following content from the text file:

    {file_content}
    """
                }
            ],
            "anthropic_version": "bedrock-2023-05-31"
        })

        print("Sending request to Bedrock API...")
        response = bedrock.invoke_model(body=body, modelId="anthropic.claude-3-haiku-20240307-v1:0")
        print("Request to Bedrock API successful.")
        return response

    except Exception as e:
        print(f"Error in send_prompt: {e}")
        raise

# Create podcast script
def create_script(pdf_name):
    try:
        print("Calling send_prompt to generate script...")
        response = send_prompt(pdf_name)

        print("Reading Bedrock API response body...")
        # Parse the response body
        response_body = json.loads(response.get("body").read())
        print(f"Response body: {response_body}")

        # Extract the content from the response
        response_data = response_body.get("content", [])
        if not response_data:
            raise ValueError("No content found in the Bedrock API response.")

        text_content = response_data[0]['text']

        # Construct output paths
        scripts_base_folder = os.path.join(TEMP_FILES_PATH, "scripts_output_folder")
        pdf_script_folder = os.path.join(scripts_base_folder, pdf_name)

        # Ensure necessary directories exist
        ensure_directories_exist(scripts_base_folder, [pdf_name])

        # Save the script to a file
        script_file_path = os.path.join(pdf_script_folder, f"{pdf_name}_script.txt")
        print(f"Saving text content to: {script_file_path}")
        with open(script_file_path, 'w', encoding='utf-8') as file:
            file.write(text_content)

        print(f"Text saved to {script_file_path}")

    except Exception as e:
        print(f"Error in create_script: {e}")
        raise
