import boto3
import json
import os

bedrock = boto3.client(service_name="bedrock-runtime")

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def send_prompt(pdf_name):

    file_content = read_file(f'pdf_2_script/extracted_text/{pdf_name}/{pdf_name}.txt')

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

    response = bedrock.invoke_model(body=body, modelId="anthropic.claude-3-haiku-20240307-v1:0")
    return response

def create_script(pdf_name):
    response = send_prompt(pdf_name)

    response_body = json.loads(response.get("body").read())
    response_data = response_body.get("content")
    text_content = response_data[0]['text']

    folder_path = os.path.join("pdf_2_script/scripts", pdf_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f"{pdf_name}_script.txt")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text_content)

    print(f"Text saved to {file_path}")
