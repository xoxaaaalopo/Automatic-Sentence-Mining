import pickle
import os
import csv
from audio_extractor import extract_audio
from subtitle_parser import get_timestamps
from dictionary_lookup import get_definitions
from import_to_anki import add_note

def run_anki_gen_pipeline(sub_file, audio_file):
    with open('anki_data.pkl', 'rb') as file:
        data = pickle.load(file)

    cards = []
    target_words = data.keys()

    for word in target_words:
        target_sentences = data[word]

        for sentence in target_sentences:
            start_time, end_time = get_timestamps(sub_file, sentence)

            audio_path = f'media/{word}_{start_time}.mp3'
            extract_audio(audio_file, start_time, end_time, audio_path)

            # image_path = f'{target_word}_{start_time}.jpg'
            # extract_screenshot('audio.mp4', start_time, image_path)

            definitions = get_definitions(word)

            # cards.append([f'[sound:{os.path.basename(audio_path)}]', target_word, definition, 
            #     f'<image src='{os.path.basement{image_path}}'>', sentence])

            cards.append([f'[sound:{os.path.basename(audio_path)}]', word, definitions, sentence])

    with open('anki_cards.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(cards)

    with open('anki_cards.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            result = add_note(row)
            print(result)
