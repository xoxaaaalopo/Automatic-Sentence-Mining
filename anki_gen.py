import pickle
import os
from audio_extractor import extract_audio
from subtitle_parser import get_timestamps

with open('anki_data.pkl', 'rb') as file:
    data = pickle.load(file)

target_word = 'peppy'
target_sentences = data[target_word]

cards = []

for sentence in target_sentences:
    start_time, end_time = get_timestamps('audio.srt', sentence)

    audio_path = f'{target_word}_{start_time}.mp3'
    extract_audio('output.mp3', start_time, end_time, audio_path)

# image_path = f'{target_word}_{start_time}.jpg'
# extract_screenshot('audio.mp4', start_time, image_path)

# definition = get_definition(target_word)

# cards.append([f'[sound:{os.path.basename(audio_path)}]', target_word, definition, 
# f'<image src='{os.path.basement{image_path}}'>', target_sentence])