"""
script to return a password based on certain choices like length and special characters.
"""

from random import choice
from string import ascii_letters, digits, punctuation


def creating_password(length, is_specialcharacter):
    """
    Generates passowrd with certain length and special characters.
    """
    character = digits + ascii_letters

    if is_specialcharacter is True:
        character = character + punctuation

    return "".join(choice(character) for every_character in range(length))
