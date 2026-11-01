import re

MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   'Æ': '·-·-', 'Ø': '---.', 'Å': '·--·-',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-', '_': '..--.-',
                   '(': '-.--.', ')': '-.--.-'}


def convert_to_morse_code(origin: str, destination: str):
    with open(origin, "r") as f:
        lines = f.readlines()
    lines = [re.sub(r'\W+', '', line) for line in lines]
    lines = [encrypt(line) for line in lines if line and len(line) > 0]
    with open(destination, 'w+') as f:
        f.writelines(lines)


def encrypt(message: str) -> str:
    cipher = ''
    for letter in message.upper():
        if letter == ' ':
            cipher += ' '
        elif letter in MORSE_CODE_DICT:
            # Characters without a Morse code are skipped rather than failing the whole build.
            cipher += MORSE_CODE_DICT[letter] + ' '
    return cipher
