from moviepy.editor import VideoFileClip
import os

def convertToWav(videoId):
    video_path = os.path.join("https://res.cloudinary.com/djw9xl2nt/video/upload/", videoId )
  

    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.join(current_directory, '..')
    audio_directory = os.path.join(parent_directory, 'Audio')
    audio_path = os.path.join(audio_directory, f"{videoId}.wav")  
    print("Audio Path :",audio_path)
    video = VideoFileClip(video_path)
    audio = video.audio

    audioFile = audio.write_audiofile(audio_path, codec='pcm_s16le')
    return os.path.join(audio_directory, f"{videoId}.wav")  
