import base64
import requests
import os
import json
import re
import toml

max_tokens_img = 1100 # per each image (kor +300)
# OpenAI API Key
api_key = ""
with open("api_secrets.toml", "r") as f:
    secrets = toml.load(f)
    api_key = secrets["openai"]["api_key"]

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_dir = "documents/image_sample/Images1"
json_template_path = "documents/json/visual_tag_en.json"
json_template_kor_path = "documents/json/visual_tag_ko.json"

# Read json file
with open(json_template_path, 'r') as file:
    json_template_eng = json.load(file)
    
# Read json file
with open(json_template_kor_path, 'r') as file:
    json_template_kor= json.load(file)
    
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
    
    prompt = f"""You are an expert in analyzing commercial videos, capable of thoroughly explaining camera techniques, the number of people present in the current shot, and other such elements. If the image contains only text or simple things, provide anaylsis simply. Here is the list of elements (explain in Korean) [if applicable]: {json.dumps(json_template_kor)}"""

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
    return response_json['choices'][0]['message']['content']

# Analyzing each image and storing responses in a list
responses = []
for i, image_path in enumerate(image_files):
    response_content = analyze_image(image_path)
    responses.append({
        "image_number": i + 1,
        "image_path": image_path,
        "analysis": response_content
    })
    print(f"Analyzed {image_path}")

# Saving responses to a text file
with open("image_analysis.txt", "w") as txt_file:
    for response in responses:
        txt_file.write(f"Image {response['image_number']}: {response['image_path']}\n")
        txt_file.write(f"Analysis:\n{response['analysis']}\n")
        txt_file.write("\n" + "="*40 + "\n\n")

# Saving responses to a JSON file
with open("image_analysis.json", "w") as json_file:
    json.dump(responses, json_file, indent=4)

# Printing all responses
for response in responses:
    print(f"Image {response['image_number']}: {response['image_path']}\nAnalysis: {response['analysis']}\n")
