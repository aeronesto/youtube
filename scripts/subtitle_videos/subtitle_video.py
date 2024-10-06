## Imports
import whisper
from functools import partial
import pandas as pd
from moviepy.editor import VideoFileClip
import moviepy.editor as mp
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import os
from datetime import datetime
current_time = datetime.now().strftime("%y-%m-%d-%H-%M-%S")

def display_subtitles(ig_width,txt):
    
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
    
    text_background_clip = ColorClip(
        size=text_clip.size,  # set to text box dimensions
        color=(29, 79, 129) # background color
    ).set_position('center').set_opacity(0.7)
    
    return CompositeVideoClip([text_background_clip, text_clip])

def subtitle_video(input_video_path, input_image_path):
    
    tmp_path = "./scripts/subtitle_videos/tmp"

    video_basename = os.path.basename(input_video_path)
    video_filename = os.path.splitext(video_basename)[0]
    audio_path = f'{tmp_path}/{current_time}-{video_filename}.mp3'

    # load video
    video_clip = mp.VideoFileClip(input_video_path)
    
    # extract audio
    video_clip.audio.write_audiofile(audio_path)
    
    # load transcriber model
    model = whisper.load_model('medium')

    # transcribe the audio
    result = model.transcribe(
        audio_path,
        task = 'translate',
        word_timestamps=True
        )

    # create segments for phrases
    dict1 = {'start':[], 'end':[], 'text':[]}
    for segment in result['segments']:
        dict1['start'].append(segment['start'])
        dict1['end'].append(segment['end'])
        dict1['text'].append(segment['text'])
    df = pd.DataFrame.from_dict(dict1)
    df.to_csv(f'{tmp_path}/subs.csv')
    
    # load previously saved subs file
    # df = pd.read_csv(f'{tmp_path}/subs.csv', header=0, names=['start', 'end', 'text'], dtype={'start': float, 'end': float})

    # create video with input image
    image_clip = ImageClip(input_image_path, duration=video_clip.duration).set_fps(video_clip.fps)
    image_clip_width, image_clip_height = image_clip.size
    
    # create subtitles with segments
    subs = tuple(zip(zip(df['start'].values, df['end'].values), df['text'].values))
    generator = partial(display_subtitles, image_clip_width)
    subtitles = SubtitlesClip(subs, generator)
    
    # create final video of image with subtitles and original audio
    final_clip = CompositeVideoClip([image_clip, subtitles.set_pos(('center'))])

    final_clip = final_clip.set_audio(video_clip.audio)
    
    final_clip.write_videofile(f'{tmp_path}/{current_time}-{video_basename}', fps=image_clip.fps, remove_temp=True, codec="libx264", audio_codec="aac")

input_video_path = './scripts/subtitle_videos/tmp/massive_lion.mp4'
input_image_path = './scripts/subtitle_videos/tmp/lion.png'
subtitle_video(input_video_path, input_image_path)