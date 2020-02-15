from pychord import Chord
import numpy as np
from scipy.io import wavfile
from functools import reduce
import math
from typing import List, Dict
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

def save_wavefile(chord_signal):
    wave_signals = 0.1*(chord_signal)
    wave = (wave_signals * float(2 ** 15 - 1)).astype(np.int16)
    wavfile.write('Dadd9.wav', SAMPLING_RATE, wave)

def translate_chord(chord_symbol: str):
    notes = analyze_chord(chord_symbol)
    frequency_list = translate_to_freauencies(notes)
    return compose_note(frequency_list)

if __name__ == '__main__':
    chord = translate_chord('Gadd9')
    save_wavefile(chord)