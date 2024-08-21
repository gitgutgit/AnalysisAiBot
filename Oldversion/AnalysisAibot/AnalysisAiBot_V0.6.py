#@Author gitgutgit

import base64
import requests
import json
import toml
import os
import streamlit as st
import re

# Streamlit title and instructions
st.title('Image to JSON Summarizer')
st.write('Upload images, specify the JSON template path, and set the output file name.')

############# Direction or Path setting #############
# Streamlit file inputs
image_dir = st.text_input('Enter the directory containing the images:', 'documents/image_sample/Images1')
json_template_path = st.text_input('Enter the path to the JSON template:', 'documents/json/visual_tag_en.json')
json_example_template_path=st.text_input('Enter the path to the JSON sample answer:', "documents/json/response_sample.json")
output_file_name = st.text_input('Enter the output file name:', 'response.json')



# Open files to read the API key and JSON template
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

# Get img path from dir
image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f)) and f != '.DS_Store']

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}




#define the functions
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]
  
#sort before base64 encoding
image_files.sort(key=natural_sort_key)

# Construct the prompt

# base64 인코딩된 이미지들을 저장할 리스트
base64_images = [encode_image(image_path) for image_path in image_files]
#base64_image = encode_image(image_files[0])
content = [
    {
        "type": "text",
        "text": f"""
         Please tag them according to the provided JSON format.
        {json.dumps(json_template_eng)}

        Example answer (this answer not related to below images):

    {json.dumps(json_example_template_eng)}
   Below images are frames taken from an advertisement video.
"""
    }
] + [
    {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    } for base64_image in base64_images
]
   





payload = {
   "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": content
        }
    ],
  "max_tokens": 4000
}

# # Streamlit button to generate summary
# if st.button('Generate Summary'):
#     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
#     summary = response.json()
    
#     # Save the response to a JSON file
#     with open(output_file_name, 'w') as outfile:
#         json.dump(summary, outfile, indent=4)
    
#     st.success(f'Summary generated and saved to {output_file_name}')

# Function to call the OpenAI API
def get_response(payload, headers):
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

# Streamlit button to trigger the API call
if st.button('Generate Summary'):
    response_json = get_response(payload, headers)
    st.write(response_json)

    # Save the raw response JSON to a file
    with open('raw_response.json', 'w', encoding='utf-8') as f:
        json.dump(response_json, f, ensure_ascii=False, indent=4)

    # Extract the JSON content from the response
    if "choices" in response_json and len(response_json["choices"]) > 0:
        response_content = response_json["choices"][0]["message"]["content"]
        
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
            with open(output_file_name, 'w', encoding='utf-8') as f:
                json.dump(response_data, f, ensure_ascii=False, indent=4)

            st.success(f"Response saved to {output_file_name}")
        except json.JSONDecodeError as e:
            st.error("Error decoding JSON")
            st.write(response_content)
    else:
        st.error("No valid response received")
