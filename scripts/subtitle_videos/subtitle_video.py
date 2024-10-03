## Imports
from __future__ import unicode_literals
from IPython.display import Video
import whisper
import cv2
from functools import partial
import pandas as pd
from moviepy.editor import VideoFileClip
import moviepy.editor as mp
from IPython.display import display, Markdown
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import os
from datetime import datetime
current_time = datetime.now().strftime("%y-%m-%d-%H-%M-%S")

"""
This script allows you to create captioned videos, replacing the original video with an image.
"""

def display_lyrics(ig_width, txt):

    text_clip = TextClip(
        txt=txt,
        font='P052-Bold', # install other fonts with ImageMagick
        fontsize=int(ig_width / 15),  # set font size (reduce to fit the box)
        stroke_width=4,  # stroke width for better visibility
        color='white',
        align='center',  # center align the text
        size=(int(ig_width * 0.8), None),  # Fix width and auto-adjust height
        method='caption'  # method to create multiline text
    ).set_position('center')

    txt_width, txt_height = text_clip.size
    
    text_background_clip = ColorClip(
        size=(int(txt_width*1.1), int(txt_height*1.1)),
        color=(135, 206, 235)
    ).set_position('center').set_opacity(0.8)
    
    return CompositeVideoClip([text_background_clip, text_clip])

def subtitle_video(input_video_path, input_image_path):
    tmp_path = "./scripts/subtitle_videos/tmp"

    # Use local clip
    video_basename = os.path.basename(input_video_path)
    video_filename = os.path.splitext(video_basename)[0]
    audio_path = f'{tmp_path}/{current_time}-{video_filename}.mp3'

    # load video
    my_clip = mp.VideoFileClip(input_video_path)
    
    # save audio from video
    my_clip.audio.write_audiofile(audio_path)

    # Instantiate whisper model using model_type variable
    model_type = 'medium'
    model = whisper.load_model(model_type)
    
    # Get text from speech for subtitles from audio file
    result = model.transcribe(
        audio_path,
        task = 'translate',
        word_timestamps=True
        )
    
    # create Subtitle dataframe, and save it
    dict1 = {'start':[], 'end':[], 'text':[]}
    # Q: what is the format of result['segments']? result['segments']['words'] contains a list of words just like segments contains segments with start, end, text
    for i in result['segments']:
        dict1['start'].append(int(i['start']))
        dict1['end'].append(int(i['end']))
        dict1['text'].append(i['text'])
    df = pd.DataFrame.from_dict(dict1)
    df.to_csv(f'{tmp_path}/subs.csv')

    # load previously saved subs file
    # df = pd.read_csv(f'{tmp_path}/subs.csv', header=0, names=['start', 'end', 'text'], dtype={'start': int, 'end': int})

    # load input video
    video_clip = VideoFileClip(input_video_path)
    duration = video_clip.duration

    # create video with input image
    image_clip = ImageClip(input_image_path, duration=duration).set_fps(video_clip.fps)
    
    ig_width, ig_height = image_clip.size      

    # create and format subtitles with SubtitlesClip
    generator = partial(display_lyrics, ig_width)
    # Q: are these cascaded tuple, zip necessary?
    subs = tuple(zip(tuple(zip(df['start'].values, df['end'].values)), df['text'].values))
    subtitles = SubtitlesClip(subs, generator)

    # create final video with input image and subtitles centered
    final = CompositeVideoClip([image_clip, subtitles.set_pos(('center'))])

    # set audio from original video
    final = final.set_audio(video_clip.audio)
    
    # save final video
    final.write_videofile(f'{tmp_path}/{current_time}-{video_basename}', fps=image_clip.fps, remove_temp=True, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    input_image_path = './scripts/subtitle_videos/tmp/lion.png'
    input_video_path = './scripts/subtitle_videos/tmp/massive_lion.mp4'
    # dir_name = os.path.splitext(os.path.basename(input_video_path))[0]
    subtitle_video(input_video_path, input_image_path)