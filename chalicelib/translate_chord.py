from pychord import Chord
import numpy as np
from functools import reduce
import math
from typing import List, Dict
import itertools

SECONDS = 3.0
BASE_FREQUENCY = 440 # A=440Hz
SCALE = [ 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#' ]

def analyze_chord(symbol: str) -> List[str]:
    chord = Chord(symbol)
    return chord.components()

def make_frequency_list(note_indexes: List[int]) -> List[float]:
    return [ BASE_FREQUENCY * 2 ** ( i / 12 ) for i in note_indexes ]

def accumulate_note_order(prev: List[int], next: int) -> List[int]:
    octave = math.floor(prev[-1] / len(SCALE)) * len(SCALE) if len(prev) > 0 else 0
    interval = octave + next
    if len(prev) > 0 and prev[-1] > interval:
        interval = interval + len(SCALE)
        prev.append(interval)
    else:
        prev.append(interval)
    return prev

def make_note_index_list(chords: List[str]) -> List[int]:
    note_indexes = [ SCALE.index(chord) for chord in chords ]
    return reduce(accumulate_note_order, note_indexes, [])

def make_frequency_map(notes: List[str]) -> Dict[str, float]:
    note_index_list = make_note_index_list(notes)
    frequency_list = make_frequency_list(note_index_list)
    return { note_name: frequency for note_name, frequency in zip(notes, frequency_list) }

def compose_note(notes: List[str]):
    pass

if __name__ == '__main__':
    notes = analyze_chord('G11')
    frequency_map = make_frequency_map(notes)
    print(frequency_map)
