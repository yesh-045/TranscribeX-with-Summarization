# Video Transcription and Summarization

This project aims to transcribe video files and add the text subtitles and can be summarize the content using generative AI.
#Sample:


https://github.com/user-attachments/assets/1df1285b-bcd3-4c76-87ab-a45872513639



## Overview

The project consists of two main functionalities:

1. **Video Transcription**: Upload a video file, which will be converted into text subtitles (VTT format). The transcription process involves converting the video to audio, then utilizing speech-to-text technology to generate subtitles.

2. **Summarization**: After transcribing the subtitles, the content is summarized using generative AI. The summary provides a concise and meaningful representation of the video content.

## Requirements

- Python 3.x
- Flask
- Cloudinary (for video handling)
- Google Generative AI (for text summarization)

## Installation

1. Clone the repository:


git clone <https://github.com/yesh-045/Video-Transcription-and-Summarzation.git>


## File Structure

- *app.py*: Flask application for handling web requests and routes.

- *summarization.py*: Python script for text summarization using Google Generative AI.

- *videoToText*: Folder containing scripts for video to text conversion.

- *audioToSubtitle*: Folder containing scripts for audio to subtitle conversion.

- *templates*: HTML templates for the web application.

- *static*: Static assets (CSS, images, etc.).


## Usage

1.*Start the Flask server:*
    python app.py
    
2.*Access the application via web browse*r at http://localhost:5000.

3.*Upload a video file for transcription.*
         The process will generate subtitles and display them along with a summary of the content.

4.*Interact with the chatbot to ask questions about the summary.*


## Contributors
1.yesh-045

2.surya54101q
