import requests
import json
import time
import os
import cloudinary
import cloudinary.uploader
# config = aai.TranscriptionConfig(language_detection=True)

# Configure Cloudinary
cloudinary.config(
    cloud_name="djw9xl2nt",
    api_key="631834537852849",
    api_secret="sA2jWjTcm9HrIK1piRkirg-OVvo"
)

base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization": "59f605b72dab4832849beed024124aa1" 
}

def upload_subtitle_to_cloudinary(subtitle_text, video_id):
    # Upload the subtitle file to Cloudinary
    result = cloudinary.uploader.upload(subtitle_text, public_id=f"{video_id}.vtt", resource_type="raw")
    return result['secure_url']

def audioToSubtitle(audioFile, video_id):
    audioFile = audioFile
    with open(audioFile, "rb") as f:
        response = requests.post(base_url + "/upload",
                        headers=headers,
                        data=f
                    )  # Set timeout to None
  # Set timeout to None

    upload_url = response.json()["upload_url"]

    data = {
        "audio_url": upload_url
    }

    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)  # Set timeout to None
    transcript_id = response.json()['id']
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()  # Set timeout to None

        if transcription_result['status'] == 'completed':
            break

        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)

    def get_subtitle_file(transcript_id, file_format):
        if file_format not in ["srt", "vtt"]:
            raise ValueError("Invalid file format. Valid formats are 'srt' and 'vtt'.")

        url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}/{file_format}"

        response = requests.get(url, headers=headers)  # Set timeout to None

        if response.status_code == 200:
            return response.text
    

    def createSubtitleFile(subtitle_text, file_path):
        
        with open(file_path, 'w') as f:
            f.write(subtitle_text)
            return file_path



    subtitle_text = get_subtitle_file(transcript_id, "vtt")
    # print("Subtitle Text: ", subtitle_text)

    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.join(current_directory, '..')
    audio_directory = os.path.join(parent_directory, 'backend-flask','static', 'SubtitleFiles')
    audio_path = os.path.join(audio_directory, f"{video_id}.vtt")

    subtitle_file = createSubtitleFile(subtitle_text, audio_path)
    print("Subtitle File: ", subtitle_file)

    
    subtitle_url = upload_subtitle_to_cloudinary(subtitle_file, video_id)
    print("Subtitle URL: ", subtitle_url)

    return subtitle_url
