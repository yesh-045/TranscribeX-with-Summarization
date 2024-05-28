from flask import Flask, render_template, request, url_for, session, redirect, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
import sys
import tempfile
from summarization import summarize_file, summarize_text ,download_file # Ensure this is correctly pointing to your summarization.py
sys.path.append('..')

from videoToText.vid_to_wav.converter import convertToWav
from audioToSubtitle.main import audioToSubtitle

app = Flask(__name__)
app.secret_key = 'sjpa&@012'

cloudinary.config(
  cloud_name="djw9xl2nt",
  api_key="631834537852849",
  api_secret="sA2jWjTcm9HrIK1piRkirg-OVvo"
)

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith(('.mp4', '.avi', '.mov')):
        result = cloudinary.uploader.upload(file, resource_type="video")
        video_id = result['public_id']
        print("Video ID: ", video_id)
        session['video_id'] = video_id
        return redirect(url_for('convertToAudio', video_id=video_id))
    return redirect(url_for('upload'))

@app.route('/convertToAudio/<video_id>')
def convertToAudio(video_id):
    audio_path = convertToWav(video_id)
    session['audio_path'] = audio_path
    print("Audio Path: ", audio_path)
    return redirect(url_for('convertToSubtitle'))

@app.route('/convertToSubtitle')
def convertToSubtitle():
    audio_path = session.get('audio_path')
    video_id = session.get('video_id')
    subtitle_url = audioToSubtitle(audio_path, video_id)
    session['subtitle_url'] = subtitle_url
    return redirect(url_for('play_video', video_id=video_id))

@app.route('/play_video/<video_id>')
def play_video(video_id):
    subtitle_url = session.get('subtitle_url')
    return render_template('play_video.html', video_id=video_id, subtitle_url=subtitle_url)

@app.route('/summarize')
def summarize():
    subtitle_url = session.get('subtitle_url')
    if subtitle_url:
        # Create a temporary file to save the subtitle content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.vtt') as tmp_file:
            tmp_file_path = tmp_file.name
            download_file(subtitle_url, tmp_file_path)
        
        summary = summarize_file(tmp_file_path)
        session['summary'] = summary
        os.remove(tmp_file_path)  # Clean up the temporary file
        return redirect(url_for('chat'))
    return "Subtitle file not found"

@app.route('/chat')
def chat():
    summary = session.get('summary', "No summary available")
    return render_template('summarize.html', summary=summary)

@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    summary = session.get('summary', "No summary available")
    if question:
        response = summarize_text(f"Q: {question}\nContext: {summary}")
        return jsonify({'response': response})
    return jsonify({'error': 'Invalid input'}), 400

if __name__ == '__main__':
    app.run(debug=True)
