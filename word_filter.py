import numpy as np
from wordfreq import zipf_frequency
import pickle
import re
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import google.generativeai as genai
import ast

lemmatizer = WordNetLemmatizer()
genai.configure(api_key='AIzaSyBNSyZBB2DVXIAIxeKXW1DbQQkldvRJ3M4')
model = genai.GenerativeModel(
    'gemini-2.5-flash-lite-preview-06-17', 
    generation_config=genai.GenerationConfig(
        temperature = 0
        # top_p = 0.1
    )
)

# Create a set of English words from a dictionary (1 time set-up)
# For user words filtering
def load_dic(wordlist):
    valid_words = set()
    count = 0
    with open(wordlist, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.split('/')[0].lower()
            if word:
                valid_words.add(word)
    return valid_words

# Save the set 
def save_dic_set(word_set, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(word_set, file)

# Load the set
def load_dic_set(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def lemmatize_word(word):
    return lemmatizer.lemmatize(word)

# Filter out non-English words 
def filter_user_words(user_words_file, word_set):
    filtered_user_words = set()

    with open(user_words_file, 'r', encoding='utf-8') as file:
        for line in file:
            cleaned_line = re.sub(r"[^a-zA-Z'\s]", ' ', line)
            cleaned_line = re.sub(r"\b(\w+)'s\b", r"\1", cleaned_line)
            words = cleaned_line.lower().split()

            for word in words:
                lemma = lemmatize_word(word)
                if lemma in word_set:
                    filtered_user_words.add(lemma)
                    
    return filtered_user_words

# Basically the same as filter_user_words
# Only not filtering out the words that aren't in the dictionary
def filter_sub_words(sub_file):
    filtered_sub_words = set()

    with open(sub_file, 'r', encoding='utf-8') as file:
        for line in file:
            cleaned_line = re.sub(r"[^a-zA-Z'\s]", ' ', line)
            cleaned_line = re.sub(r"\b(\w+)'s\b", r"\1", cleaned_line)
            words = cleaned_line.lower().split()

            for word in words:
                lemma = lemmatize_word(word)
                filtered_sub_words.add(lemma)

    return filtered_sub_words

def calculate_coverage_by_zipf(known_words_set, all_words_set):
    bins = [(8, 7), (7, 6), (6, 5), (5, 4), (4, 3), (3, 2), (2, 1), (1, 0)] 
    coverage = {}

    # As it is now, it's processing the entire English dictionay every time. 
    for upper, lower in bins:
        # Pick out words for the current bin
        words_in_bin = []
        for word in all_words_set:
            if lower < zipf_frequency(word, 'en') <= upper:
                words_in_bin.append(word)

        if words_in_bin:
            # known_in_bin = [word for word in words_in_bin if word in known_words_set]    
            known_in_bin = []
            for word in words_in_bin:
                if word in known_words_set:
                    known_in_bin.append(word)
            percentage = (len(known_in_bin) / len(words_in_bin)) * 100

        else:
            percentage = 0  # No words in this bin

        coverage[f'{upper}~{lower}'] = round(percentage, 2)

    return coverage

def bin_words_by_zipf(words_set):
    bins = {
        '8~7': [],
        '7~6': [],
        '6~5': [],
        '5~4': [],
        '4~3': [],
        '3~2': [],
        '2~1': [],
        '1~0': []
    }

    for word in words_set:
        freq = zipf_frequency(word,'en')
        if 7 < freq <= 8:
            bins['8~7'].append(word)
        elif 6 < freq <= 7:
            bins['7~6'].append(word)
        elif 5 < freq <= 6:
            bins['6~5'].append(word)
        elif 4 < freq <= 5:
            bins['5~4'].append(word)
        elif 3 < freq <= 4:
            bins['4~3'].append(word)
        elif 2 < freq <= 3:
            bins['3~2'].append(word)
        elif 1 < freq <= 2:
            bins['2~1'].append(word)
        elif 0 < freq <= 1:
            bins['1~0'].append(word)
    
    return bins

def calculate_user_coverage(known_words_set, binned_words):
    coverage = {}

    for bin_label, words in binned_words.items():
        if words:
            known_in_bin = [word for word in words if word in known_words_set]
            percentage = (len(known_in_bin) / len(words)) * 100
        else:
            percentage = 0
        
        coverage[bin_label] = round(percentage, 2)
    
    return coverage

def get_potential_learning_words(known_words_set, subs_words_set, dict_words_set):
    bins_order = ['8~7', '7~6', '6~5', '5~4', '4~3', '3~2', '2~1', '1~0']

    binned_dict_words = bin_words_by_zipf(dict_words_set) # Optimizable
    dict_coverage = calculate_user_coverage(known_words_set, binned_dict_words)

    skip_tiers = set()
    for idx, bin_label in enumerate(bins_order[::-1]):
        if dict_coverage[bin_label] > 10:
            skip_tiers.update(bins_order[:len(bins_order) - idx - 1])
    
    binned_subs_words = bin_words_by_zipf(subs_words_set)
    
    potential_words = []
    for bin_label in bins_order:
        if bin_label not in skip_tiers:
            unknown_words = [word for word in binned_subs_words[bin_label] if word not in known_words_set]
            potential_words.extend(unknown_words)
    
    return potential_words

def find_sentences_with_potential_words(sub_file, potential_words):
    word_to_sentences = {word: [] for word in potential_words}

    with open(sub_file, 'r', encoding='utf-8') as file:
        for line in file:
            cleaned_line = re.sub(r"[^a-zA-Z'\s]", ' ', line)
            cleaned_line = re.sub(r"\b(\w+)'s\b", r"\1", cleaned_line)
            words = cleaned_line.lower().split()
            lemmatized_words = [lemmatize_word(word) for word in words]

            for word in potential_words:
                if word in lemmatized_words:
                    word_to_sentences[word].append(line.strip())

    return word_to_sentences

def filter_with_gemini(potential_words):
    prompt = f"""
        Consider the words: "{potential_words}"

        Instructions:
        - Discard the word if 
            1) it's a proper noun (e.g. Daniel, Tokyo, Google, etc)
            2) it's self-explanatory (e.g. wash-able, light-weight, over-cooked, important-ly, etc)
            3) it's not a real English word (e.g. uhh, mmm, yaaay, smth, relix, etc)
        - Respond only with an array of words that you did not discard
        - Do NOT explain anything or add any extra text

        Example response: ['decrepit', 'levitate', 'concoction']
        """
    response = model.generate_content(prompt)
    
    return response.text

if __name__ == '__main__':
    # word_set = load_dic('en_US.dic')
    # save_dic_set(word_set, 'english_words.pkl')

    input_file = 'known_words.txt'
    english_dict = load_dic_set('english_words.pkl')

    filtered_sub_words = filter_sub_words('audio.srt')
    filtered_user_words = filter_user_words(input_file, english_dict)
    # print(filtered_user_words)

    words = get_potential_learning_words(filtered_user_words, filtered_sub_words, english_dict)
    # print(find_sentences_with_potential_words('audio3.srt', words))
    # print(words)
    # user_vocabulary_coverage = calculate_coverage_by_zipf(filtered_user_words, english_dict)
    
    final_words = ast.literal_eval(filter_with_gemini(words))
    final_sentences = find_sentences_with_potential_words('audio.srt', final_words)

    with open('anki_data.pkl', 'wb') as file:
        pickle.dump(final_sentences, file)

def run_word_filter_pipeline(sub_file, user_word_file, english_dict_file):
    english_dict = load_dic_set(english_dict_file)

    filtered_user_words = filter_user_words(user_word_file, english_dict)
    filtered_sub_words = filter_sub_words(sub_file)

    words = get_potential_learning_words(filtered_user_words, filtered_sub_words, english_dict)

    final_words = ast.literal_eval(filter_with_gemini(words))
    final_sentences = find_sentences_with_potential_words(sub_file, final_words)

    with open('anki_data.pkl', 'wb') as file:
        pickle.dump(final_sentences, file)



# ========== Embedding Code (Archived) =============
# from sklearn.metrics.pairwise import cosine_similarity
# # Load GloVe txt file into a dictionary (1 time set-up)
# def load_glove_txt(file_path):
#     embeddings = {}
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             values = line.split()
#             word = values[0]
#             vector = np.asarray(values[1:], dtype='float32')
#             embeddings[word] = vector
#     return embeddings

# def save_glove_embeddings(embeddings, file_path):
#     with open(file_path, 'wb') as file:
#         pickle.dump(embeddings, file)

# def load_glove_embeddings(file_path):
#     with open(file_path, 'rb') as file:
#         return pickle.load(file)

# def compute_embeddings(words, glove_embeddings):
#     vectors = []
#     for word in words:
#         if word in glove_embeddings:
#             vectors.append(glove_embeddings[word])
#         else:
#             vectors.append(np.zeros(300))
#     return np.array(vectors)

# glove_embeddings = load_glove_embeddings('glove_embeddings.pkl')
   
# word = 'importantly'
# known_enbeddings = compute_embeddings(filtered_user_words, glove_embeddings)
# new_word_embedding = compute_embeddings([word], glove_embeddings)

# similarities = cosine_similarity(new_word_embedding, known_enbeddings)
# max_sim = np.max(similarities)

# print(f"New word: {word}")
# print(f"Max similarity: {max_sim}")
# =============================================================