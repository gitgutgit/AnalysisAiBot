import streamlit as st
import base64
import requests
import os
import json
import re
import toml
from collections import defaultdict

# OpenAI API Key
api_key = ""
with open("api_secrets.toml", "r") as f:
    secrets = toml.load(f)
    api_key = secrets["openai"]["api_key"]

max_tokens_img = 1100  # per each image (kor +300)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to calculate the cost
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

# For sorting
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# Function to analyze an image
def analyze_image(image_path, language):
    base64_image = encode_image(image_path)
    explain_language = "Korean" if language == "kor" else "English"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = f"""You are an expert in analyzing commercial videos, capable of thoroughly explaining camera techniques, the number of people present in the current shot, and other such elements. If the image contains only text or simple things, provide analysis simply. Here is the list of elements (explain in {explain_language}) [if applicable]: {json.dumps(json_template, ensure_ascii=False)}"""

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
def tag_images(analyses, temperature):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt2 = f"""
    Please create tags for the following analyses according to the provided JSON format.
    {json.dumps(json_template)}

    Example answer (this answer not related to below images):

    {json.dumps(json_example_answer)}

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
        "max_tokens": 4000,  # Adjust max tokens if necessary
        "temperature": temperature
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

# Streamlit App
st.title("Image Analysis and Tagging")

# Input for image directory
image_dir = st.text_input("Enter the image folder path:", "documents/image_sample/Images4")
image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f)) and f != '.DS_Store']
image_files.sort(key=natural_sort_key)

# Select language for JSON template
language = st.selectbox("Select the JSON template language:", ["en", "kor"])
json_template_path = f"documents/json/visual_tag_{language}.json"
json_example_answer_path = f"documents/json/response_sample_{language}.json"

# Read json files
with open(json_template_path, 'r', encoding='utf-8') as file:
    json_template = json.load(file)

with open(json_example_answer_path, 'r', encoding='utf-8') as file:
    json_example_answer = json.load(file)

# Input for temperature
temperature = st.slider("Select the temperature for the tagging function:", 0.0, 1.0, 0.3)

# Input for save directory and base filename
save_dir = st.text_input("Enter the save folder path:", "results/")
base_filename = st.text_input("Enter the base filename for saving results:", "0000")

if st.button("Analyze Images"):
    # Ensure save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    responses = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    analyses = []

    for i, image_path in enumerate(image_files):
        response_content, prompt_tokens, completion_tokens = analyze_image(image_path, language)
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
        st.write(f"Analyzed {image_path}")

    # Tagging images based on all analyses
    tagged_responses = tag_images(analyses, temperature)

    # File paths
    txt_file_path = os.path.join(save_dir, f"{base_filename}_analysis.txt")
    json_file_path = os.path.join(save_dir, f"{base_filename}_analysis.json")
    tag_json_file_path = os.path.join(save_dir, f"{base_filename}_tag.json")

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

    # Displaying results
    st.write("Image analysis and tagging completed!")
    st.write(f"Results saved to:\n- {txt_file_path}\n- {json_file_path}\n- {tag_json_file_path}")

    # Calculating total cost
    total_cost = calculate_cost(total_prompt_tokens, total_completion_tokens)
    st.write(f"Total cost for processing {len(image_files)} images: {total_cost:.2f} KRW")
