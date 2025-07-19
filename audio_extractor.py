import subprocess
import os
import shutil

def extract_audio(input_file, start_time, end_time, output_file):
    duration = 0.1 + end_time - start_time
    cmd = [
        'ffmpeg', '-y',
        '-i', input_file,
        '-ss', str(start_time),
        '-t', str(duration),
        output_file
    ]
    subprocess.run(cmd, check=True)
    copy_to_anki_media(output_file)

# copies the given file to Anki's collection.media folder
def copy_to_anki_media(file_path):
    anki_media_path = os.path.expanduser('~/Library/Application Support/Anki2/User 11/collection.media')

    if os.path.exists(anki_media_path):
        shutil.copy(file_path, os.path.join(anki_media_path, os.path.basename(file_path)))
    else:
        print(f'Could not find Anki media folder: {anki_media_path}')