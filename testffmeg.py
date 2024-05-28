import pandas

input_file = 'videoToText/Audio/y0c3xn6iyqnh5umzqmuq.wav'
output_file = 'backend-flask/static/SubtitleFiles/y0c3xn6iyqnh5umzqmuq.vtt'

ffmpeg.input(input_file).output(output_file, format='vtt').run()
