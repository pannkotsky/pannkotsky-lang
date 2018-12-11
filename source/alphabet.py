import string

from tokens import tokens

LETTERS = string.ascii_lowercase
DIGITS = list(map(str, range(10)))

ALPHABET = set()
ALPHABET.update(LETTERS)
ALPHABET.update(DIGITS)
for t, _ in tokens:
    ALPHABET.update(list(t))
