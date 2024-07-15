import base64
import requests
import os
import json
import re
import toml
from collections import defaultdict

max_tokens_img = 1100  # per each image (kor +300)
prompt_tokens = 0
# OpenAI API Key
api_key = ""
with open("api_secrets.toml", "r") as f:
    secrets = toml.load(f)
    api_key = secrets["openai"]["api_key"]

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to calculate the cost   1Dollar = 1340KRW 
def calculate_cost(prompt_tokens, completion_tokens):
    return (prompt_tokens / 1000000 * 0.5 + completion_tokens / 1000000 * 1.5) * 1340

# Function to generate a new file name if the file already exists
def get_new_file_name(file_path):
    base, ext = os.path.splitext(file_path)
    counter = 1
    new_file_path = f"{base}_{counter}{ext}"
    while os.path.exists(new_file_path):
        counter += 1
        new_file_path = f"{base}_{counter}{ext}"
    return new_file_path

# Path to your image
image_dir = "documents/image_sample/Images4" # change this directory to the directory where your images are stored
json_template_path = "documents/json/visual_tag_en.json"
json_template_kor_path = "documents/json/visual_tag_ko.json"
json_example_answer_path = "documents/json/response_sample.json"
json_example_answer_kor_path = "documents/json/response_sample_kor.json"

# Read json files
with open(json_template_path, 'r', encoding='utf-8') as file:
    json_template_eng = json.load(file)

with open(json_template_kor_path, 'r', encoding='utf-8') as file:
    json_template_kor = json.load(file)

with open(json_example_answer_path, 'r', encoding='utf-8') as file:
    json_example_answer = json.load(file)

with open(json_example_answer_kor_path, 'r', encoding='utf-8') as file:
    json_example_answer_kor = json.load(file)

# For sorting
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# Getting the base64 string
image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f)) and f != '.DS_Store']

# Sorting the image files
image_files.sort(key=natural_sort_key)
print("List of image_files: ", image_files)

print("=====================================")
print("=====================================")

# Function to analyze an image
def analyze_image(image_path):
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = f"""You are an expert in analyzing commercial videos, capable of thoroughly explaining camera techniques, the number of people present in the current shot, and other such elements. If the image contains only text or simple things, provide analysis simply. Here is the list of elements (explain in Korean) [if applicable]: {json.dumps(json_template_kor, ensure_ascii=False)}"""

    content = [
        {
            "type": "text",
            "text": prompt
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }
    ]

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "max_tokens": max_tokens_img  # Adjust max tokens if necessary
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json = response.json()

    prompt_tokens = response_json['usage']['prompt_tokens']
    completion_tokens = response_json['usage']['completion_tokens']

    return response_json['choices'][0]['message']['content'], prompt_tokens, completion_tokens

# Function to tag images based on analyses
def tag_images(analyses):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt2 = f"""
    Please create tags for the following analyses according to the provided JSON format.
    {json.dumps(json_template_kor)}

    Example answer (this answer not related to below images):

    {json.dumps(json_example_answer_kor)}

    Below image analyses are taken from an advertisement video:
    {json.dumps(analyses, ensure_ascii=False)}
    """

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": prompt2
            }
        ],
        "max_tokens": 4000  # Adjust max tokens if necessary
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    # Debugging step to check response content
    try:
        response_json = response.json()
        print("Response JSON:", response_json)
        
        # Remove code block notation and load JSON
        content = response_json['choices'][0]['message']['content']
        if content.startswith('```json'):
            content = content[7:-4].strip()
        
        return json.loads(content)
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e)
        print("Response text:", response.text)
        return {}

# Analyzing each image and storing responses in a list
responses = []
total_prompt_tokens = 0
total_completion_tokens = 0
analyses = []

for i, image_path in enumerate(image_files):
    response_content, prompt_tokens, completion_tokens = analyze_image(image_path)
    total_prompt_tokens += prompt_tokens
    total_completion_tokens += completion_tokens
    analyses.append({
        "image_number": f"{i + 1:03}",
        "analysis": response_content
    })
    responses.append({
        "image_number": i + 1,
        "image_path": image_path,
        "analysis": response_content,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens
    })
    print(f"Analyzed {image_path}")

# Tagging images based on all analyses
tagged_responses = tag_images(analyses)

# File paths
txt_file_path = "image_analysis.txt"
json_file_path = "image_analysis.json"
tag_json_file_path = "tag.json"

# Generate new file names if they already exist
if os.path.exists(txt_file_path):
    txt_file_path = get_new_file_name(txt_file_path)
if os.path.exists(json_file_path):
    json_file_path = get_new_file_name(json_file_path)
if os.path.exists(tag_json_file_path):
    tag_json_file_path = get_new_file_name(tag_json_file_path)

# Saving responses to a text file
with open(txt_file_path, "w", encoding='utf-8') as txt_file:
    for response in responses:
        txt_file.write(f"Image {response['image_number']}: {response['image_path']}\n")
        txt_file.write(f"Analysis:\n{response['analysis']}\n")
        txt_file.write(f"Prompt Tokens: {response['prompt_tokens']}, Completion Tokens: {response['completion_tokens']}\n")
        txt_file.write("\n" + "="*40 + "\n\n")

# Saving responses to a JSON file
with open(json_file_path, "w", encoding='utf-8') as json_file:
    json.dump(responses, json_file, indent=4, ensure_ascii=False)

# Saving tagged responses to a separate JSON file
with open(tag_json_file_path, "w", encoding='utf-8') as tag_json_file:
    json.dump(tagged_responses, tag_json_file, indent=4, ensure_ascii=False)

# Printing all responses
for response in responses:
    print(f"Image {response['image_number']}: {response['image_path']}\nAnalysis: {response['analysis']}\n")
    print(f"Prompt Tokens: {response['prompt_tokens']}, Completion Tokens: {response['completion_tokens']}\n")

# Calculating total cost
print("==========================\n \n \n")
total_cost = calculate_cost(total_prompt_tokens, total_completion_tokens)
print(f"Total cost for processing {len(image_files)} images: {total_cost:.2f} KRW")
