import re

OPERATION_KEYWORD = '演奏して'

def extract_chord(text: str) -> str:
    result = re.match('^{}\n([A-G][a-z0-9]*)'.format(OPERATION_KEYWORD), text)
    return result.group(1) if result is not None else ''

if __name__ == "__main__":
    pass