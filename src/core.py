"""
This module provides the PasswordGenerator class for generating secure passwords.
"""

import os
from random import shuffle, uniform
from secrets import choice
from string import ascii_letters, digits, punctuation
import logging
from dotenv import load_dotenv

load_dotenv()


class PasswordGenerator:
    """
    A class to generate secure passwords.
    """

    def is_valid(self, length: int) -> bool:
        """
        Validate the password length.

        Args:
            length (int): Length of the password to be generated.

        Raises:
            ValueError: If the length is less than 8 or greater than 128.

        Returns:
            bool: True if the length is valid, False otherwise.
        """
        MIN_LENGTH = int(os.getenv("MIN_LENGTH", 8))
        MAX_LENGTH = int(os.getenv("MAX_LENGTH", 128))

        if length < MIN_LENGTH:
            raise ValueError(
                f"Password length should be at least {MIN_LENGTH} characters."
            )
        if length > MAX_LENGTH:
            raise ValueError(
                f"Password length should not exceed {MAX_LENGTH} characters."
            )
        return True

    def generate_password(
        self,
        length: int,
        include_letters: bool = False,
        include_special: bool = False,
        include_digits: bool = False,
    ) -> str:
        """
        Generate a secure password.

        Args:
            length (int): Length of the password to be generated.
            include_letters (bool, optional): whether to include letters in the password. Defaults to True.
            include_special (bool, optional): whether to include special characters in the password. Defaults to True.
            include_digits (bool, optional): whether to include digits in the password. Defaults to True.

        Raises:
            ValueError: If the length is less than 8 or greater than 128.

        Returns:
            str: Generated password.
        """
        self.is_valid(length)

        if not (include_letters or include_special or include_digits):
            raise ValueError("At least one character type must be included.")

        character_pool: list = []
        distribution: int = length

        if include_letters and include_special and include_digits:
            if include_letters:
                include_letter_distribution = int(distribution * uniform(0.2, 0.4))
                character_pool.append(
                    [choice(ascii_letters) for _ in range(include_letter_distribution)]
                )
                distribution -= include_letter_distribution
            if include_special:
                include_special_distribution = int(distribution * uniform(0.2, 0.4))
                character_pool.append(
                    [choice(punctuation) for _ in range(include_special_distribution)]
                )
                distribution -= include_special_distribution
            if include_digits:
                character_pool.append([choice(digits) for _ in range(distribution)])
        else:
            if include_letters and include_special:
                if include_letters:
                    include_letter_distribution = int(distribution * uniform(0.2, 0.6))
                    character_pool.append(
                        [
                            choice(ascii_letters)
                            for _ in range(include_letter_distribution)
                        ]
                    )
                    distribution -= include_letter_distribution
                if include_special:
                    character_pool.append(
                        [choice(punctuation) for _ in range(distribution)]
                    )
            elif include_letters and include_digits:
                if include_letters:
                    include_letter_distribution = int(distribution * uniform(0.2, 0.6))
                    character_pool.append(
                        [
                            choice(ascii_letters)
                            for _ in range(include_letter_distribution)
                        ]
                    )
                    distribution -= include_letter_distribution
                if include_digits:
                    character_pool.append([choice(digits) for _ in range(distribution)])
            elif include_special and include_digits:
                if include_special:
                    include_special_distribution = int(distribution * uniform(0.2, 0.6))
                    character_pool.append(
                        [
                            choice(punctuation)
                            for _ in range(include_special_distribution)
                        ]
                    )
                    distribution -= include_special_distribution
                if include_digits:
                    character_pool.append([choice(digits) for _ in range(distribution)])
            else:
                if include_letters:
                    character_pool.append(
                        [choice(ascii_letters) for _ in range(distribution)]
                    )
                if include_special:
                    character_pool.append(
                        [choice(punctuation) for _ in range(distribution)]
                    )
                if include_digits:
                    character_pool.append([choice(digits) for _ in range(distribution)])

        character_pool = [item for sublist in character_pool for item in sublist]
        shuffle(character_pool)
        password = "".join(character_pool)
        logging.info(f"Generated a password of length {length}.")
        return password
