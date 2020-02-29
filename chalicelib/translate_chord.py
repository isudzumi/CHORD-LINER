from pychord import Chord
import numpy as np
from scipy.io import wavfile
from functools import reduce
import math
from typing import List
import itertools

SECONDS = 2.0
BASE_FREQUENCY = 440 # A=440Hz
SAMPLING_RATE = 44100
SCALE = [ 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#' ]

def analyze_chord(symbol: str) -> List[str]:
    chord = Chord(symbol)
    return chord.components()

def make_frequency_list(note_indexes: List[int]) -> List[float]:
    return [ BASE_FREQUENCY * 2 ** ( i / 12 ) for i in note_indexes ]

def get_current_octave(interval: int) -> int:
    return math.floor(interval / len(SCALE)) * len(SCALE)

def raise_octave(order: int) -> int:
    return order + len(SCALE)

def accumulate_note_order(intervals: List[int], order: int) -> List[int]:
    current_octave = get_current_octave(intervals[-1]) if len(intervals) > 0 else 0
    interval = current_octave + order
    if len(intervals) > 0 and intervals[-1] > interval:
        interval = raise_octave(interval)
    intervals.append(interval)
    return intervals

def make_note_index_list(chords: List[str]) -> List[int]:
    note_indexes = [ SCALE.index(chord) for chord in chords ]
    return reduce(accumulate_note_order, note_indexes, [])

def translate_to_freauencies(notes: List[str]) -> List[float]:
    note_index_list = make_note_index_list(notes)
    return make_frequency_list(note_index_list)

def create_sin_wave(frequency: float):
    phases = np.cumsum(2.0 * np.pi * frequency / SAMPLING_RATE * np.ones(int(SAMPLING_RATE * SECONDS)))
    return np.sin(phases)

def compose_note(frequencies: List[float]):
    translate = np.frompyfunc(create_sin_wave, 1, 1)
    sin_waves = translate(frequencies)
    return np.sum(sin_waves, axis=0)

def translate_chord(chord_symbol: str):
    notes = analyze_chord(chord_symbol)
    if not notes:
        return {}
    frequency_list = translate_to_freauencies(notes)
    return {
        'signals': compose_note(frequency_list),
        'duration': int(SECONDS * 1000),
        'sampling_rate': SAMPLING_RATE
    }

if __name__ == '__main__':
    pass