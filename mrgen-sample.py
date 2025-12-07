
import os
import json
import sys
from datetime import datetime
from typing import Iterable, Tuple, Optional
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import base64
from openai import AzureOpenAI

OUTPUT_DIR = "./out"
OUTPUT_BASENAME = "synthetic_ehr_"

TEMPERATURE = 0.7
MAX_TOKENS = 4096  # enough to return ~100 JSON objects with small fields

def_endpoint = "https://rws-openai-mcs.cognitiveservices.azure.com/"
def_deployment = "gpt-4.1"
#def_api_version = "2024-12-01-preview"
def_api_version = "2025-03-01-preview"

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_client() -> AzureOpenAI:

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT",def_endpoint)
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT",def_deployment)
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", def_api_version)
    
    client = AzureOpenAI(
        azure_ad_token_provider=token_provider,        
        api_version=api_version,
        azure_endpoint=endpoint,
    )
    model = deployment  # in Azure, 'model' == your deployment name
    return client, model, "azure"

def generate_output(prompt_text: str, input_data_path: str) -> str:    
    client, model, provider = get_client()

    file = client.files.create(
        file=open(input_data_path, "rb"),
        purpose="assistants")
    print(f"Uploaded file id: {file.id}")


    messages = [
        {"role": "system", "content": "You are a clinical data synthesis model."},
        {"role": "user", 
         "content": [

                {
                    "type": "input_text",
                    "text": prompt_text,
                },            
            ],
         "attachments": [
                { "file_id": file.id }
            ],
        },
        ]

    kwargs = dict(
        model=model,
        input=messages,
        #temperature=TEMPERATURE,
        #max_tokens=MAX_TOKENS,
    )
    response = client.responses.create(**kwargs)
    #

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content

def main(prompt_path: str, input_data_path: str, output_path: str) -> None:
    prompt_text = load_prompt(prompt_path)
    response = generate_output(prompt_text,input_data_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python mrgen.py conditional_prompt.txt input_data.csv output.txt")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
