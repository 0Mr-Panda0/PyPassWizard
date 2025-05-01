"""
Test case for PasswordGenerator class.
This test case covers the following functionalities:
- Validating password length
- Generating passwords with different options
- Generating passwords with and without special characters
"""

import pytest
from src.core import PasswordGenerator
from string import punctuation


class TestPasswordGenerator:
    """
    Test cases for the PasswordGenerator class.
    """

    def setup_method(self):
        """
        Setup method for the test cases.
        """
        self.generator = PasswordGenerator()

    def test_is_valid_with_valid_length(self):
        """
        Test if the password length is valid.
        """
        assert self.generator.is_valid(8) is True
        assert self.generator.is_valid(128) is True

    def test_is_valid_with_invalid_length(self):
        """
        Test if the password length is invalid.
        """
        with pytest.raises(
            ValueError, match="Password length should be at least 8 characters."
        ):
            self.generator.is_valid(7)
        with pytest.raises(
            ValueError, match="Password length should not exceed 128 characters."
        ):
            self.generator.is_valid(129)

    def test_generate_password_default_options(self):
        """
        Test password generation with default options.
        """
        password = self.generator.generate_password(
            12, include_letters=True, include_digits=True, include_special=True
        )
        assert len(password) == 12
        assert any(char.isalpha() for char in password)
        assert any(char.isdigit() for char in password)
        assert any(char in punctuation for char in password)

    def test_generate_password_without_special_characters(self):
        """
        Test password generation without special characters.
        """
        password = self.generator.generate_password(
            10, include_letters=True, include_special=False, include_digits=True
        )
        assert len(password) == 10
        assert any(char.isalpha() for char in password)
        assert any(char.isdigit() for char in password)
        assert not any(char in punctuation for char in password)

    def test_generate_password_without_digits(self):
        """
        Test password generation without digits.
        """
        password = self.generator.generate_password(
            10, include_letters=True, include_special=True, include_digits=False
        )
        assert len(password) == 10
        assert any(char.isalpha() for char in password)
        assert not any(char.isdigit() for char in password)
        assert any(char in punctuation for char in password)

    def test_generate_password_without_letters(self):
        """
        Test password generation without letters.
        """
        password = self.generator.generate_password(
            10, include_letters=False, include_special=True, include_digits=True
        )
        assert len(password) == 10
        assert not any(char.isalpha() for char in password)
        assert any(char.isdigit() for char in password)
        assert any(char in punctuation for char in password)
