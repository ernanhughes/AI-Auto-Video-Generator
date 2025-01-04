import openai
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Load your API key from an environment variable or a .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_story(prompt):
    """Generate a story based on the given prompt using OpenAI's GPT-4 model."""

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use 'gpt-4' for the best creative writing model
        messages=[
            {"role": "system", "content": "You are a creative writing assistant."},
            {"role": "user", "content": f'Can you please improve this prompt to make it produce the best story possible : {prompt}'}
        ],
        max_tokens=400,  # Adjust as per your desired length
        temperature=0.7,  # Controls randomness; adjust for creativity
    )

    final_story_prompt = response.choices[0].message['content'].strip()

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use 'gpt-4' for the best creative writing model
        messages=[
            {"role": "system", "content": "You are a creative writing assistant."},
            {"role": "user", "content": final_story_prompt}
        ],
        max_tokens=400,  # Adjust as per your desired length
        temperature=0.7,  # Controls randomness; adjust for creativity
    )
    story = response.choices[0].message['content'].strip()
    return story, final_story_prompt

def save_story_with_image_prompts(story, prompt, image_prompts):
    with open(f"story_{timestamp}.txt", "w") as f:
        f.write(prompt + "\n" + story + "\n\nImage Prompts:\n")
        for idx, image_prompt in enumerate(image_prompts, start=1):
            f.write(f"{idx}: {image_prompt}\n")

def save_story(story):
    file_path = f"story_{timestamp}.txt"
    with open(file_path, "w") as f:
        f.write(story)
    return file_path  # Return the file path where the story is saved

