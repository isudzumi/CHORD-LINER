from pychord import Chord
import numpy as np
from typing import List
import itertools

SECONDS = 3.0
BASE_FREQUENCY = 440 # A=440Hz
MAX_RANGE = 28

def analyze_chord(symbol: str) -> List[str]:
    chord = Chord(symbol)
    return chord.components()

def make_frequency_list() -> List[float]:
    return [ BASE_FREQUENCY * 2 ** ( i / 12 ) for i in range(0, MAX_RANGE) ]

def make_note_name_list():
    NOTE_NAMES = [ 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#' ]
    tone_names = [ note + str(i) for i, note in itertools.product(range(4, 7), NOTE_NAMES) ]
    return tone_names[0:MAX_RANGE]

def make_frequency_map():
    frequency_list = make_frequency_list()
    note_name_list = make_note_name_list()
    return { note_name: frequency for note_name, frequency in zip(note_name_list, frequency_list) }

def compose_note(notes: List[str]):
    pass

if __name__ == '__main__':
    notes = analyze_chord('Aadd9')
    print(notes)