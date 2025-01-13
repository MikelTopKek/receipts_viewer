

from typing import Any


class BaseLogger:
    """Print logger class"""

    def __init__(self, *args) -> None:
        pass

    @staticmethod
    def log(*args: dict[str, Any], level: str = "debug") -> None:
        """Base log implementation using simple print"""
        print(args, level)

