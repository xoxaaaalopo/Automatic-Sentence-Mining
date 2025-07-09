import subprocess

def extract_audio(input_file, start_time, end_time, output_file):
    duration = end_time - start_time
    cmd = [
        'ffmpeg', '-y',
        '-i', input_file,
        '-ss', str(start_time),
        '-t', str(duration),
        '-c', 'copy',
        output_file
    ]
    subprocess.run(cmd, check=True)