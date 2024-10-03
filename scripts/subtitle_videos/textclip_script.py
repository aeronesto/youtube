## Imports
from moviepy.editor import *
from datetime import datetime

current_time = datetime.now().strftime("%y-%m-%d-%H-%M-%S")

def create_image_with_text(input_image_path):
    # Load the input image
    image_clip = ImageClip(input_image_path)

    # Get the dimensions of the image
    ig_width, ig_height = image_clip.size

    # Create a TextClip with the specified width
    text_clip = TextClip(
        txt="Did you ever hear about that island where the river broke off into a different direction and made this area an island in Africa?",
        font='P052-Bold',  # specify the font
        fontsize=int(ig_width / 15),  # set font size (reduce to fit the box)
        stroke_width=4,  # stroke width for better visibility
        color='white',
        align='center',  # center align the text
        size=(int(ig_width * 0.8), None),  # Fix width and auto-adjust height
        method='caption'  # method to create multiline text
    ).set_position('center')

    # Create a colored background for the text box
    text_background_clip = ColorClip(
        size=text_clip.size,  # set to text box dimensions
        color=(29, 79, 129) # background color
    ).set_position('center').set_opacity(0.7)

    # Composite the text and background onto the image
    final_clip = CompositeVideoClip([image_clip, text_background_clip, text_clip])

    # Save the resulting frame as an image
    final_clip.save_frame(f'./scripts/subtitle_videos/tmp/{current_time}-imageclip.png')

# Input image path
input_image_path = './scripts/subtitle_videos/tmp/lion.png'
create_image_with_text(input_image_path)