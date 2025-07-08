import pickle
import os

with open('anki_data.pkl', 'rb') as file:
    data = pickle.load(file)

target_word = 'peppy'
target_sentence = data[target_word]

cards = []

start_time, end_time = get_timestamps('audio.srt', target_sentence)

audio_path = f'{target_word}_{start_time}.webm'
extract_audio('audio.webm', start_time, end_time, audio_path)

image_path = f'{target_word}_{start_time}.jpg'
extract_screenshot('audio.mp4', start_time, image_path)

definition = get_definition(target_word)

cards.append([f'[sound:{os.path.basename(audio_path)}]', target_word, definition, 
f'<image src='{os.path.basement{image_path}}'>', target_sentence])