import pickle

# Create a set from a wordlist
def load_wordlist(wordlist):
    valid_words = set()
    with open(wordlist, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip().split('/')[0].lower()
            if word:
                valid_words.add(word)
    return valid_words

# Save the set using pickle
def save_word_set(word_set, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(word_set, file)

def load_word_set(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def filter_user_words(user_words, word_set):
    filtered_user_words = set()

    with open(user_words, 'r', encoding='utf-8') as file:
        for line in file:
            words = ''.join(char if char.isalpha() or char == ' ' 
                else ' ' for char in line).lower().split()

            for word in words:
                if word in word_set:
                    filtered_user_words.add(word)
    return list(filtered_user_words)

if __name__ == '__main__':
    # word_set = load_wordlist('en_US.dic')
    # save_word_set(word_set, 'english_words.pkl')
    input_file = 'known_words.txt'
    english_words_set = load_word_set('english_words.pkl')

    filtered_words = filter_user_words(input_file, english_words_set)

    print(len(filtered_words))