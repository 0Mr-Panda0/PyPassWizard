# PyPassWizard

Welcome to **PyPassWizard**! This is a command-line application designed to generate and securely store passwords. It is lightweight, easy to use, and perfect for managing your passwords directly from the terminal.

## Features

- Generate strong, random passwords of customizable length.
- Store passwords securely in an encrypted database.
- Retrieve stored passwords by name or tag.
- Delete passwords securely.
- User-friendly CLI interface with clear commands and options.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/0Mr-Panda0/PyPassWizard.git
    ```

2. Navigate to the project directory:

    ```bash
    cd PyPassWizard
    ```

3. Install the required dependencies:

    ```bash
    uv sync
    ```

4. Run the application:

    ```bash
    uv run PyPassWizard.py --help
    ```

## Usage

Here are some examples of how to use PyPassWizard:

### Generate a Password

Generate a random password with a specified length:

```bash
uv run PyPassWizard.py generate -l 13 -i yes -c yes -d yes
```

### Store a Password

Store a password with a name for easy retrieval:

```bash
uv run PyPassWizard.py store --name "GitHub" --password "mySecurePassword123!"
```

### Retrieve a Password

Retrieve a stored password by its name:

```bash
uv run PyPassWizard.py retrieve --name "GitHub"
```

### Delete a Password

Delete a stored password securely:

```bash
uv run PyPassWizard.py delete --name "GitHub"
```

### View Help

View all available commands and options:

```bash
uv run PyPassWizard.py --help
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a pull request.

## Roadmap

Here are some planned features for future releases:

- Password strength checker.
- Export and import passwords in encrypted formats.
- Multi-language support for CLI messages.
- Integration with cloud storage for password backups.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact me at [Karan Behera](mailto:karan.behera366@gmail.com).

Thank you for using PyPassWizard!

[![CI Pipeline](https://github.com/0Mr-Panda0/PyPassWizard/actions/workflows/main.yml/badge.svg)](https://github.com/0Mr-Panda0/PyPassWizard/actions/workflows/main.yml)
