import requests

def add_note(fields):
    payload = {
        'action': 'addNote',
        'version': 6,
        'params': {
            'note': {
                'deckName': 'Migaku Audio Cards',
                'modelName': 'Migaku Japanese CUSTOM STYLING copy',
                'fields': {
                    'Sentence': fields[0],
                    'Target Word': fields[1],
                    'Definitions': fields[2],
                    'Sentence Audio': fields[3]
                }
            }
        }
    }
    response = requests.post('http://localhost:8765', json=payload)
    return response.json()