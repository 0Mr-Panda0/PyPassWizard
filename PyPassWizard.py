import logging
import os
from src.cli import CLIApp


def main() -> None:
    """
    Main function to run the CLI application.
    This function sets up the logging configuration and initializes the CLI application.
    """
    # Ensure the logs directory exists
    logs_dir = os.path.join(os.path.dirname(__file__), "log")
    os.makedirs(logs_dir, exist_ok=True)

    # Configure logging to write only to a file
    log_file = os.path.join(logs_dir, "app.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file)  # Log only to the file
        ],
    )

    cli = CLIApp()
    cli_command = cli.get_command()
    cli_command()


if __name__ == "__main__":
    main()
