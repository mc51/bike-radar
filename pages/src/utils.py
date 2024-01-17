"""Utilities"""
from logging import Formatter
import re


class RedactingFormatter(Formatter):  # pylint: disable=too-few-public-methods
    """Redact sensitive strings from logs."""

    def __init__(self, orig_formatter):  # pylint: disable=super-init-not-called
        self.orig_formatter = orig_formatter
        self.patterns = ["email", "mobile", "loginkey", "login_key", "pin"]

    def format(self, record) -> str:
        """Format record by replacing all values of keys corresponding to pattern.

        Args:
            record (_type_): record

        Returns:
            str: redacted message
        """
        msg: str = self.orig_formatter.format(record)
        msg = msg.replace("'", '"')

        for pattern in self.patterns:
            p = rf'"{pattern}":\s*"([^"]+)"'
            match = re.search(p, msg)
            if match:
                secret = match.group(1)
                msg = msg.replace(str(secret), "***redacted***")
        return msg

    def __getattr__(self, attr):
        return getattr(self.orig_formatter, attr)
