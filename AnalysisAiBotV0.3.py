#@Author gitgutgit

import base64
import requests
import json
import toml
import time 
import os

############# Direction or Path setting #############
# Directory containing the images
image_dir = "documents/image_sample/Images1"
    
json_template_path = "documents/json/visual_tag.json"
json_example_template_path = "documents/json/first_video_eng.json"

######## Open files to read the API key and JSON template################

with open("api_secrets.toml", "r") as f:
    secrets = toml.load(f)
    api_key = secrets["openai"]["api_key"]

# Load JSON template from file
with open(json_template_path, "r") as f:
    json_template_eng = json.load(f)
    
with open(json_example_template_path, "r") as f:
    json_example_template_eng = json.load(f)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

#print(image_files)
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
    
prompt = f"""
What’s in these images? Treat them as a single advertisement and provide a summary in JSON format using the given template:

{json.dumps(json_template_eng)}

Example answer:

{json.dumps(json_example_template_eng)}

Here are the images:
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
                }
            ] + [message["content"][1] for message in messages]
        }
    ],
    "max_tokens": 3000
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

response_json = response.json()
print(response_json)

# Save the response JSON to a file
with open('raw_response.json', 'w', encoding='utf-8') as f:
    json.dump(response_json, f, ensure_ascii=False, indent=4)

# Extract the JSON content from the response
if "choices" in response_json and len(response_json["choices"]) > 0:
    response_content = response_json["choices"][0]["message"]["content"]
    
    # Print the raw response content to debug
    print("Raw response content:")
    print(response_content)
    
    # Clean up the response content
    response_content = response_content.strip()
    if response_content.startswith('```json'):
        response_content = response_content[7:]
    if response_content.endswith('```'):
        response_content = response_content[:-3]
    
    try:
        # Load the content as a JSON object
        response_data = json.loads(response_content)
        
        # Save the response data to a file
        with open('response.json', 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)

        print("Response saved to response.json")
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        print("Response content:")
        print(response_content)
else:
    print("No valid response received")
