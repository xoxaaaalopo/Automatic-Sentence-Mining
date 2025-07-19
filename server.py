from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import re
from word_filter import run_word_filter_pipeline
from anki_gen import run_anki_gen_pipeline

app = Flask(__name__)
CORS(app)

@app.route('/generateSubs', methods=['POST'])
def generate_subtitles():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Extract video ID
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    video_id = match.group(1)

    # Download audio
    audio_file = f'{video_id}.mp3'
    subprocess.run(['yt-dlp', '-f', 'bestaudio', '--extract-audio', '--audio-format', 'mp3', '-o', '%(id)s.mp3', url], check=True)

    # Generate subtitles
    subprocess.run(['whisper', audio_file, '--model', 'base', '--language', 'English',
'--output_format', 'srt', '--word_timestamps', 'True'],check=True)
    subtitle_file = f'{video_id}.srt'

    # Run word_filter.py
    run_word_filter_pipeline(subtitle_file, 'known_words.txt', 'english_words.pkl')

    # Run anki_gen.py
    run_anki_gen_pipeline(subtitle_file, audio_file)

    return jsonify({'message': 'Subtitle generation completed'})

if __name__ == '__main__':
    app.run(port=5001)