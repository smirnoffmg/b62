import b62
import pytest


@pytest.mark.parametrize(
    "num,expected",
    [
        (0, "0"),
        (1, "1"),
        (10, "A"),
        (61, "z"),
        (62, "10"),
        (3843, "zz"),
        (238327, "zzz"),
        (123456789, "8M0kX"),
    ],
)
def test_encode(num, expected):
    encoded = b62.encode(num)
    assert encoded == expected


@pytest.mark.parametrize(
    "s,expected",
    [
        ("0", 0),
        ("1", 1),
        ("A", 10),
        ("z", 61),
        ("10", 62),
        ("zz", 3843),
        ("zzz", 238327),
        ("8M0kX", 123456789),
    ],
)
def test_decode(s, expected):
    assert b62.decode(s) == expected


def test_encode_decode_roundtrip():
    for num in [0, 1, 10, 61, 62, 123, 2023, 9999999, 2**32]:
        encoded = b62.encode(num)
        decoded = b62.decode(encoded)
        assert decoded == num


def test_decode_invalid():
    with pytest.raises(ValueError):
        b62.decode("invalid_string!")
