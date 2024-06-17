from random import choice, randint
from string import ascii_letters, digits, punctuation
from datetime import datetime


def storing_password(password):
    file_path = "password.txt"
    with open(file_path, "a+") as note:
        note.write(
            f"Password:{password} - length of password:{len(password)} - timestamp:{datetime.now()}\n"
        )


def creating_password(length_of_password=11, if_special_character_allowed="Yes"):
    if if_special_character_allowed == "Yes":
        character = digits + ascii_letters + punctuation
    else:
        character = digits + ascii_letters
    return "".join(choice(character) for every_character in range(length_of_password))