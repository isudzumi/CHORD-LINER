from typing import Dict
from chalicelib.extract_chord import extract_chord
from chalicelib.translate_chord import translate_chord
from chalicelib.save_file import save_file

def get_chord(event):
    chord = extract_chord(event.message.text)
    if not chord:
        return {}
    audio = translate_chord(chord)
    audio.update({
        'file_name': '{}.wav'.format(chord)
    })
    response = save_file(audio)
    if not response:
        return {}
    return {
        'url': response.url,
        'duration': audio.duration
    }

if __name__ == "__main__":
    pass