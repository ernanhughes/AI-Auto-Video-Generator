import time
import os
from story_generator import generate_story, save_story_with_image_prompts, save_story
from keyword_identifier import extract_image_prompts
from image_generator import generate_images, save_images
from voiceover_generator import generate_voiceover, save_voiceover
from video_creator import create_video
from caption_generator import (
    extract_story_from_file,
    create_caption_images,
    add_captions_to_video,
)

OUTPUT_DIR = "output"

def main():
    timestamp = int(time.time())
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Get user input
    story_prompt = input("Enter a story prompt: ")

    story, final_story_prompt = generate_story(
        story_prompt
    )  # Update the assignment to get the final_story_prompt
    print(f"Story generated successfully.\n {story} \n{final_story_prompt}")

    # Generate image Prompts
    image_prompts = extract_image_prompts(story)
    print("Image prompts extracted.")

    # Save the story and image prompts together
    save_story(OUTPUT_DIR, final_story_prompt)  # save story alone for captions
    save_story_with_image_prompts(OUTPUT_DIR, 
        story, final_story_prompt, image_prompts
    )  # Use final_story_prompt instead of story_prompt

    # Generate images
    images = generate_images(image_prompts)
    print("Images generated successfully.")
    save_images(OUTPUT_DIR, images, timestamp)

    # Generate the voiceover
    voiceover = generate_voiceover(story)
    if voiceover:
        print("Voiceover generated successfully.")
        save_voiceover(OUTPUT_DIR, voiceover, timestamp)
    else:
        print("Voiceover generation failed.")

    # Create the video
    create_video(OUTPUT_DIR, images, voiceover, story, timestamp)
    print("Video created successfully.")

    story_file_path = save_story(OUTPUT_DIR, story)

    # Prompt user to add captions
    add_captions_option = input(
        "Do you want to add captions to the video? (y/n): "
    ).lower()

    if add_captions_option == "y":

        # Extract the story from the file
        story = extract_story_from_file(story_file_path)

        # Convert story segments to caption images
        caption_images = create_caption_images(story)

        # Path for the newly created video with captions
        video_with_captions_path = f"{OUTPUT_DIR}/video_with_captions_{timestamp}.mp4"

        # Overlay captions onto the video
        add_captions_to_video(
            f"output_video_{timestamp}.mp4", caption_images, video_with_captions_path
        )
        print("Captions added successfully.")


if __name__ == "__main__":
    main()
