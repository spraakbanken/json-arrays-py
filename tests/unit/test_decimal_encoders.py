from decimal import Decimal
from json_streams.encoders import encode_decimal
from json_streams import jsonlib


def test_encode_decimal():
    result = jsonlib.dumps([10.20, '10.20', Decimal('10.20')], default=encode_decimal)

    assert result == jsonlib.dumps([10.20, '10.20', 10.20])

