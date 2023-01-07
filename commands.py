import importlib
import inspect
import string
from typing import Optional, Callable

from thefuzz import fuzz, process


class Command:
    def __init__(self, name: str, func: Callable):
        self.name = name.lower().replace("_", " ").strip()
        self.func = func

    def execute(self, *args, **kwargs):
        self.func(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.execute(*args, **kwargs)


class CommandFailedError(Exception):
    """Raise when an executed command fails"""


def register_commands(modules: list[str]) -> list[Command]:
    commands = []
    for module_name in modules:
        module = importlib.import_module(module_name)
        for func_name, func in inspect.getmembers(module, inspect.isfunction):
            commands.append(Command(name=func_name, func=func))

    return commands


def preprocess_transcript(phrase: str) -> str:
    """remove punctuation and trailing whitespaces"""
    return phrase.lower().strip().translate(str.maketrans("", "", string.punctuation))


def check_keyword(phrase: str, keyword: str) -> Optional[str]:
    tokens = list(filter(None, phrase.split(" ")))
    if tokens[0] == keyword:
        return " ".join(tokens[1:]).strip()
    else:
        return None


def parse_phrase(phrase: str, commands: list[Command]) -> tuple[Command, str]:
    result = process.extract(phrase, (c.name for c in commands), scorer=fuzz.token_sort_ratio, limit=2)
    # TODO add threshold for command matching certainty
    top_command_name = result[0][0]  # select the top match result
    command = next((c for c in commands if c.name == top_command_name))
    arguments = phrase.removeprefix(top_command_name).strip()
    return command, arguments


def execute_command(transcript, keyword, commands_config):
    if not (phrase := preprocess_transcript(transcript)):
        # raise ValueError("Preprocessed transcript is `None`")
        return None

    if not (phrase := check_keyword(phrase, keyword)):
        # raise ValueError(f"Keyword {keyword} not found")
        return None

    command, args = parse_phrase(phrase, commands_config)
    try:
        command.execute(args)
    except CommandFailedError:
        print(f"{command.name}: execution failed")
