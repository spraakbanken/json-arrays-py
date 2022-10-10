import pytest


@pytest.fixture(name="entries")
def fixture_entries() -> list[dict]:
    return [
        {"a": "b"},
        {"a": {"b": 2}},
    ]
