from typing import Dict, List

import pytest


@pytest.fixture(name="entries")
def fixture_entries() -> List[Dict]:
    return [
        {"a": "b"},
        {"a": {"b": 2}},
    ]
