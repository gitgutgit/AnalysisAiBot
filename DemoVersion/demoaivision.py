#@Author gitgutgit

import base64
import requests
import json
import toml
import time 
import os

with open("api_secrets.toml", "r") as f:
    secrets = toml.load(f)
    api_key = secrets["openai"]["api_key"]


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Directory containing the images
image_dir = "documents/image_sample/Images1"



image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

print(image_files)
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

messages = []
# Process each image and add to messages
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    base64_image = encode_image(image_path)
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"What’s in this image? {image_file}"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
    })
    
    
payload = {
  "model": "gpt-4o",
  "messages": messages,
  "max_tokens": 250 *len(image_files)
}


response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())
