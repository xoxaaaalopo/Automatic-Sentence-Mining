from nltk.corpus import wordnet

# nltk.download('omw-1.4')

def get_definitions(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return "No definition found."
    return synsets[0].definition()

# ==== Get definitions through Free Dictionary API (Archived)======
# import requests
# def get_definitions(word):
#     url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()

#         meanings = data[0].get('meanings', [])
#         if not meanings: return 'No definition found.'

#         definitions = meanings[0].get('definitions', [])
#         if not definitions: return 'No definition found.'

#         return definitions[0].get('definition', 'No defiition found.')
    
#     except requests.exceptions.RequestException as e:
#         return f'API error: {e}'
#     except (KeyError, IndexError):
#         return "Key error or index error"