from setuptools import setup, find_packages  # type: ignore
import os
from dotenv import load_dotenv

load_dotenv()

setup(
    name="PyPassWizard",
    version="0.3.2",
    author="0Mr-Panda0",
    author_email="karan.behera366@gmail.com",
    description="A CLI application for managing passwords securely.",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/0Mr-Panda0/PyPassWizard",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "click>=8.1.8",
        "fastparquet>=2024.11.0",
        "funkybob>=2023.12.0",
        "mypy>=1.15.0",
        "openpyxl>=3.1.5",
        "pandas>=2.2.3",
        "pandera>=0.23.1",
        "pyarrow>=20.0.0",
        "pytest>=8.3.5",
        "pytest-cov>=6.1.1",
        "ruff>=0.11.7",
        "setuptools>=80.0.0",
        "tabulate>=0.9.0",
        "twine>=6.1.0",
    ],
    entry_points={
        "console_scripts": [
            "pypasswizard=src.cli:main",
        ],
    },
)
