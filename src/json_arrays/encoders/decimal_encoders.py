"""Encoderd to use with writers."""

import decimal
from typing import Any


def encode_decimal(obj: Any) -> float:
    """Encode decimal as float."""
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
