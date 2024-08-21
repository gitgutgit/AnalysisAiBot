import base64
import requests
import os
import json
import re

import toml
# OpenAI API Key
api_key =""
with open("api_secrets.toml", "r") as f:
    secrets = toml.load(f)
    api_key = secrets["openai"]["api_key"]

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image

image_dir = "documents/image_sample/Images1"
image_path = "documents/image_sample/Images1/A1_F001.jpeg"
json_template_path = "documents/json/visual_tag_en.json"

# read json file
with open(json_template_path, 'r') as file:
    json_template_eng = json.load(file)
    
    
 # for sorting
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]
  
    
# Getting the base64 string
image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f)) and f != '.DS_Store']
#base64_image = encode_image(image_path)


# Sorting the image files
image_files.sort(key=natural_sort_key)
print("list of image_files: ", image_files)


print("=====================================")
print("=====================================")

#random select
base64_image = encode_image(image_files[2])
print(image_files[2])
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}
prompt = f""" You are an expert in analyzing commercial videos, capable of thoroughly explaining camera techniques, the number of people present in the current shot, and other such elements the list is : {json.dumps(json_template_eng)}"



"""
payload = {
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
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
    }
  ],
  "max_tokens": 500
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
# Printing only the content of the response
response_content = response.json()['choices'][0]['message']['content']
print(response_content)