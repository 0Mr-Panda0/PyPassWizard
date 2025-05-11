"""
Test case for PasswordGenerator class.
This test case covers the following functionalities:
- Validating password length
- Generating passwords with different options
- Generating passwords with and without special characters
"""

import os
import pytest
from src.core import PasswordGenerator
from string import punctuation
from dotenv import load_dotenv

load_dotenv()


class TestPasswordGenerator:
    """
    Test cases for the PasswordGenerator class.
    """

    def setup_method(self):
        """
        Setup method for the test cases.
        """
        self.generator = PasswordGenerator()

    def assert_password_properties(
        self,
        password: str,
        length: int,
        has_letters: bool,
        has_digits: bool,
        has_special: bool,
    ) -> None:
        """
        Assert the properties of a generated password.

        Args:
            password (str): The generated password.
            length (int): Expected length of the password.
            has_letters (bool): Whether the password should contain letters.
            has_digits (bool): Whether the password should contain digits.
            has_special (bool): Whether the password should contain special characters.
        """
        assert len(password) == length, "Password length does not match."
        assert any(char.isalpha() for char in password) == has_letters, (
            "Password letter presence mismatch."
        )
        assert any(char.isdigit() for char in password) == has_digits, (
            "Password digit presence mismatch."
        )
        assert any(char in punctuation for char in password) == has_special, (
            "Password special character presence mismatch."
        )

    def test_is_valid_with_valid_length(self):
        """
        Test if the password length is valid.
        """
        assert self.generator.is_valid(int(os.getenv("MIN_LENGTH", 8))) is True
        assert self.generator.is_valid(int(os.getenv("MAX_LENGTH", 128))) is True

    def test_is_valid_with_invalid_length(self):
        """
        Test if the password length is invalid.
        """
        with pytest.raises(
            ValueError, match="Password length should be at least 8 characters."
        ):
            self.generator.is_valid(int(os.getenv("MIN_LENGTH", 8)) - 1)
        with pytest.raises(
            ValueError, match="Password length should not exceed 128 characters."
        ):
            self.generator.is_valid(int(os.getenv("MAX_LENGTH", 128)) + 1)

    @pytest.mark.parametrize(
        "length, include_letters, include_digits, include_special, has_letters, has_digits, has_special",
        [
            (12, True, True, True, True, True, True),
            (10, True, True, False, True, True, False),
            (10, True, False, True, True, False, True),
            (10, False, True, True, False, True, True),
        ],
    )
    def test_generate_password(
        self,
        length,
        include_letters,
        include_digits,
        include_special,
        has_letters,
        has_digits,
        has_special,
    ):
        """
        Test password generation with various configurations.
        """
        password = self.generator.generate_password(
            length, include_letters, include_special, include_digits
        )
        self.assert_password_properties(
            password, length, has_letters, has_digits, has_special
        )

    def test_generate_password_with_no_character_types(self):
        """
        Test if generating a password with no character types raises a ValueError.
        """
        with pytest.raises(
            ValueError, match="At least one character type must be included."
        ):
            self.generator.generate_password(
                10, include_letters=False, include_special=False, include_digits=False
            )
