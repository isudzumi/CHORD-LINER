from chalicelib.extract_chord import extract_chord

def test_single_major_chord():
    assert extract_chord("演奏して\nC") == 'C'

def test_if_allow_line_feed():
    assert extract_chord('演奏してC') == 'C'

def test_no_input():
    assert extract_chord('') == ''

def test_no_chord():
    assert extract_chord('foobar') == ''

def test_plural_chord():
    assert extract_chord('演奏して\nF7G7Em7Am') == 'F7'

def test_ending_with_number():
    assert extract_chord('演奏して\nCadd9') == 'Cadd9'

def test_major_seventh():
    assert extract_chord('演奏して\nCM7') == 'CM7'
    