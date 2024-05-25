import re
import requests
import google.generativeai as genai

genai.configure(api_key="AIzaSyAlUo0FYZudT_DX-XdJuSApC9rCFrK55nA")  # Replace 'YOUR_API_KEY' with your actual API key

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config)

convo = model.start_chat(history=[])

def remove_timestamps(subtitles):
    """
    Removes timestamps from subtitle text.
        Args:
            subtitles: A string representing the subtitles content.
        Returns:
            clean_subtitles: A string with timestamps removed.
    """
    # Define the regular expression pattern to match timestamps
    timestamp_pattern = r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}'
    clean_subtitles = re.sub(timestamp_pattern, '', subtitles)
    return clean_subtitles

def summarize_text(prompt):
    """
    Summarizes the given prompt using Generative AI.

    Args:
        prompt: A string representing the prompt for summarization.

    Returns:
        summary: A string representing the summarized text.
    """
    summary = " "
    try:
        response = convo.send_message(prompt)
        if response:
            summary = convo.last.text
    except Exception as e:
        print("Error:", e)
    return summary

def download_file(url, local_filename):
    """
    Downloads a file from a URL and saves it locally.

    Args:
        url: The URL of the file to download.
        local_filename: The local path where the file should be saved.

    Returns:
        local_filename: The path to the downloaded file.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def summarize_file(file_path):
    """
    Summarizes the content of a file.

    Args:
        file_path: A string representing the path to the file that needs to be summarized.

    Returns:
        summary: A string representing the summarized text.
    """
    summary = ""
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            if file_path.endswith('.vtt'):  
                file_content = remove_timestamps(file_content)
            file_content = "Given the provided text, summarize it into a concise and meaningful paragraph, ensuring that the length of the summary is approximately half of the total number of lines in the input text. The summary should capture the main ideas and key points of the text while maintaining coherence and clarity.\n" + file_content
            summary = summarize_text(file_content)
            if summary:
                print("Summarized text:")
                print(summary)
    except FileNotFoundError:
        print("Error: File not found")
    return summary

def ask_questions(summary):
    """
    Allows the user to ask questions about the summary and receive responses.

    Args:
        summary: A string representing the summarized text.

    Returns:
        None
    """
    while True:
        question = input("\nAsk a question about the summary (type 'exit' to end): ")
        if question.lower() == 'exit':
            break
        response = summarize_text(question)
        print("Response:", response)
