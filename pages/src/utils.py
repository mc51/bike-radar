"""Utilities"""
from logging import Formatter


class RedactingFormatter(Formatter):  # pylint: disable=too-few-public-methods
    """Redact loginkey from logs."""

    def __init__(self, orig_formatter, patterns, *args, **kwargs):
        self.orig_formatter = orig_formatter
        self._patterns = patterns
        super().__init__(*args, **kwargs)

    def format(self, record) -> str:
        """Format record.

        Args:
            record (_type_): record

        Returns:
            str: redacted record
        """
        msg: str = self.orig_formatter.format(record)
        for p in self._patterns:
            pos = msg.find(p)
            if pos > 0:
                msg = msg[:pos] + " loginkey **** " + msg[pos + 30 :]
        return msg

    def __getattr__(self, attr):
        return getattr(self.orig_formatter, attr)
