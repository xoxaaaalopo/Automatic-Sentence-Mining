from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/generateSubs', methods=['POST'])
def generate_subtitles():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Download audio
    audio_file = 'audio.webm'
    subprocess.run(['yt-dlp', '-f', 'bestaudio', '-o', audio_file, '--force-overwrites', url], check=True)

    # Generate subtitles
    subprocess.run(['whisper', audio_file, '--model', 'base', '--language', 'English',
    '--output_format', 'srt'], check=True)

    return jsonify({'message': 'Subtitle generation completed'})

if __name__ == '__main__':
    app.run(port=5001)