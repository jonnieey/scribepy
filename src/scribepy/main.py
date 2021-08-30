import sys
import argparse
from pathlib import Path

from loguru import logger
from pynput import keyboard

from scribepy import custom_logger

from scribepy.cli import play_file as cli

def get_parser():
    """
    Create custom parser

    Returns: parser -> ArgumentParser
    """
    usage = "scribepy [OPTIONS] [COMMAND] [COMMAND_OPTIONS]"
    description = "Command line audio player for transcription"
    parser = argparse.ArgumentParser(
        prog="scribepy",
        usage=usage,
        description=description,
        add_help=False,
    )

    main_help = "Show this help message and exit."
    subcommand_help = "Show this help message and exit."

    global_options = parser.add_argument_group(title="Global options")
    global_options.add_argument("-h", "--help", action="help", help=main_help)
    global_options.add_argument(
        "-L",
        "--log-level",
        type=str.upper,
        help="Log level to use",
        choices=(
            "TRACE",
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ),
    )

    global_options.add_argument(
        "-P",
        "--log-path",
        metavar="",
        help="Log file to use",
    )
    global_options.add_argument("file", help="File to play")

    return parser

def main(args=None):
    parser = get_parser()
    opts = parser.parse_args(args=args)
    kwargs = opts.__dict__

    log_level = kwargs.pop("log_level")
    log_path = kwargs.pop("log_path")

    if log_path:
        log_path = Path(log_path)
        if log_path.is_dir():
            log_path = log_path / "scribepy-{time}.log"
        custom_logger(sink=log_path, level=log_level or "WARNING")
    elif log_level:
        custom_logger(sink=sys.stderr, level="WARNING")

    try:
        return cli(**kwargs)
    except Exception as error:
        logger.exception(error)
        print(error)
        sys.exit(0)

if __name__ == "__main__":
    main()
