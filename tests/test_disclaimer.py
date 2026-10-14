import pytest
from scripts.amp_validator import REQUIRED_DISCLAIMER

EXACT_DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

def test_exact_disclaimer_match():
    assert REQUIRED_DISCLAIMER == EXACT_DISCLAIMER_TEXT
