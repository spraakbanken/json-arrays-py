"""Encoders

`encode_decimal`
>>> from decimal import Decimal
>>> from json_arrays import jsonlib, encoders
>>> jsonlib.dumps([10.20, "10.20", Decimal("10.20")], default=encoders.encode_decimal)
b'[10.20,"10.20",10.20]'
"""

from .decimal_encoders import encode_decimal

__all__ = ["encode_decimal"]
