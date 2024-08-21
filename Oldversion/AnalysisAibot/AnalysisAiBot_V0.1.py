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
    
    
json_templete_eng="""
{
  "Number of People": [
    "One person",
    "One person + etc.",
    "Two people",
    "Two people + etc.",
    "10 or more people",
    "Multiple people",
    "Crowd",
    "+ etc."
  ],
  "Characters": [
    "Baby (male)",
    "Baby (female)",
    "Child (male)",
    "Child (female)",
    "Teenager (male)",
    "Teenager (female)",
    "20s (male)",
    "20s (female)",
    "30s (male)",
    "30s (female)",
    "Middle-aged gentleman",
    "Middle-aged woman",
    "Elderly (male)",
    "Elderly (female)",
    "Nude (male)",
    "Nude (female)",
    "Celebrity"
  ],
  "Ethnicity": [
    "Korean",
    "Japanese",
    "Chinese",
    "Southeast Asian",
    "Other Asian",
    "Caucasian",
    "Latino",
    "Black",
    "Middle Eastern",
    "Mixed race"
  ],
  "Screen Speed": [
    "Normal speed",
    "Slow motion",
    "Rewind",
    "Time-lapse",
    "Fast motion"
  ],
  "Technique": [
    "Parody",
    "Bizarre",
    "2D animation",
    "3D animation",
    "Character animation",
    "Cel animation",
    "Stop motion",
    "Clay animation",
    "Realistic animation",
    "Cartoonish animation",
    "Other animation",
    "Humor",
    "Home video",
    "Documentary-style",
    "Pop art",
    "Still photo",
    "Collage",
    "Testimonial",
    "Motion graphics",
    "3D",
    "Special equipment filming (Flying cam, etc.)",
    "CGI",
    "Practical effects",
    "Green screen",
    "Miniatures",
    "Matte painting",
    "Compositing"
  ],
  "Color": [
    "Color",
    "Black and white + Color (small)",
    "Black and white",
    "Monochromatic",
    "Complementary",
    "Analogous",
    "Triadic",
    "Warm",
    "Cool",
    "Pastel",
    "Vibrant"
  ],
  "Era": [
    "Present",
    "2000s",
    "90s",
    "80s",
    "70s",
    "60s",
    "50s",
    "Liberation period",
    "Japanese colonial period",
    "Future",
    "Prehistoric",
    "Joseon Dynasty",
    "Medieval",
    "Ancient Rome",
    "Ancient Greece",
    "Ancient Egypt",
    "Ancient civilization",
    "Ancient history"
  ],
  "Background": [
    "Simple (pure) background",
    "Outdoor",
    "Aerial SF",
    "Indoor",
    "Stage studio",
    "Underwater",
    "Space"
  ],
  "Perspective": [
    "First-person perspective",
    "Third-person perspective",
    "Side view",
    "Facing the camera"
  ],
  "Angle": [
    "Aerial shot",
    "Low angle shot",
    "Satellite shot",
    "Bird's eye view",
    "Big close-up",
    "Long shot",
    "Long take (one scene)"
  ],
  "Camera Movement": [
    "Static",
    "Pan",
    "Tilt",
    "Zoom",
    "Dolly",
    "Tracking",
    "Handheld",
    "Steadicam"
  ],
  "Action": [
    "Laughing",
    "Crying",
    "Hitting"
  ],
  "Emotion Expression": [
    "Pleased",
    "Lovely",
    "Satisfied",
    "Happy",
    "Angry",
    "Disappointed",
    "Frustrated",
    "Sad",
    "Serious",
    "Worried"
  ],
  "Mood": [
    "Cheerful",
    "Melancholic",
    "Mysterious",
    "Romantic",
    "Tense",
    "Calm",
    "Energetic",
    "Nostalgic"
  ],
  "Animals": [
    "Pet",
    "Livestock",
    "Puppy",
    "Dog",
    "Chicken",
    "Cow",
    "Horse",
    "Snake",
    "Mouse",
    "Dragon",
    "Sheep"
  ],
  "Lighting": [
    "Natural light",
    "Artificial light",
    "High key",
    "Low key",
    "Silhouette",
    "Backlight",
    "Soft light",
    "Hard light"
  ],
  "Composition": [
    "Rule of thirds",
    "Symmetry",
    "Leading lines",
    "Framing",
    "Patterns",
    "Golden ratio",
    "Diagonal",
    "Triangular"
  ],
  "Genre": [
    "Action",
    "Comedy",
    "Drama",
    "Horror",
    "Sci-Fi",
    "Romance",
    "Thriller",
    "Documentary",
    "Experimental"
  ],
  "Editing Style": [
    "Continuous",
    "Jump cut",
    "Montage",
    "Cross-cutting",
    "Match cut",
    "Slow disclosure"
  ],
  "Texture": [
    "Smooth",
    "Rough",
    "Grainy",
    "Glossy",
    "Matte",
    "Distressed"
  ],
  "Style": [
    "Minimalist",
    "Maximalist",
    "Vintage",
    "Modern",
    "Abstract",
    "Photorealistic",
    "Surrealist",
    "Impressionist"
  ],
  "Audio": [
    "Diegetic sound",
    "Non-diegetic sound",
    "Voice-over",
    "Soundtrack",
    "Ambient sound",
    "Sound effects"
  ],
  "Narrative Structure": [
    "Linear",
    "Non-linear",
    "Episodic",
    "Parallel",
    "Circular",
    "Frame narrative"
  ]
}
"""

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
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                     "text": "What’s in these images? Treat them as a single advertisement and provide a summary in JSON format {json_templete_eng}using the given template. Here are the images:"
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

with open('response.json', 'w', encoding='utf-8') as f:
    json.dump(response_json, f, ensure_ascii=False, indent=4)

print("Response saved to response.json")



print("===============================================")
