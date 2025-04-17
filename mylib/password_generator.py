from random import choice
from string import ascii_letters, digits, punctuation

def creating_password(length, HasSpecialCharacter):
    character = digits + ascii_letters
    if HasSpecialCharacter is True:
        character = character + punctuation
    return "".join(choice(character) for every_character in range(length))