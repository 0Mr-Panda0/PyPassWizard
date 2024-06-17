from mylib.password_generator import creating_password, storing_password
from string import punctuation
import os


def test_password_generator():
    case_1 = creating_password(12, "Yes")
    case_2 = creating_password(7, "No")
    assert len(case_1) == 12
    assert len(case_2) == 7 and punctuation not in case_2
    case_3 = storing_password(case_1)
    assert os.path.isfile("password.txt")
