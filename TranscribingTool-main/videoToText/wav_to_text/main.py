import requests
from api_02 import *
import os,sys

filename = "Audio/my_audio.wav"
audio_url = upload(filename)

save_transcript(audio_url, 'converted_text_file/converted_text.txt')