import decimal
from typing import Any


def encode_decimal(obj: Any):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
