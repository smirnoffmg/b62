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
        (2**32, "4gfFC4"),
        (2**63 - 1, "AzL8n0Y58m7"),  # Max u64 value
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
        ("4gfFC4", 2**32),
        ("AzL8n0Y58m7", 2**63 - 1),  # Max u64 value
    ],
)
def test_decode(s, expected):
    assert b62.decode(s) == expected


def test_encode_decode_roundtrip():
    test_numbers = [
        0,
        1,
        10,
        61,
        62,
        123,
        2023,
        9999999,
        2**32,
        2**48,
        2**63 - 1,  # Edge cases
    ]
    for num in test_numbers:
        encoded = b62.encode(num)
        decoded = b62.decode(encoded)
        assert decoded == num


def test_decode_invalid():
    invalid_strings = [
        "invalid_string!",
        "hello world",
        "123@456",
        "abc-def",
        "space in string",
        "unicode_🚀",
        "",  # Empty string
    ]

    for invalid_str in invalid_strings:
        with pytest.raises(ValueError):
            b62.decode(invalid_str)


def test_decode_invalid_characters():
    """Test specific invalid character handling."""
    with pytest.raises(ValueError, match="Invalid character"):
        b62.decode("abc!")


def test_decode_empty_string():
    """Test empty string handling."""
    with pytest.raises(ValueError, match="Empty string"):
        b62.decode("")


def test_encode_edge_cases():
    """Test encoding edge cases."""
    # Test powers of 62
    assert b62.encode(62**0) == "1"
    assert b62.encode(62**1) == "10"
    assert b62.encode(62**2) == "100"
    assert b62.encode(62**3) == "1000"

    # Test boundary values
    assert b62.encode(0) == "0"
    assert b62.encode(1) == "1"
    assert b62.encode(61) == "z"
    assert b62.encode(62) == "10"


def test_decode_edge_cases():
    """Test decoding edge cases."""
    # Test single characters
    assert b62.decode("0") == 0
    assert b62.decode("1") == 1
    assert b62.decode("A") == 10
    assert b62.decode("z") == 61

    # Test powers of 62
    assert b62.decode("10") == 62
    assert b62.decode("100") == 62**2
    assert b62.decode("1000") == 62**3


def test_character_set():
    """Test that all valid Base62 characters work."""
    valid_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    for i, char in enumerate(valid_chars):
        assert b62.decode(char) == i


def test_large_numbers():
    """Test encoding/decoding of very large numbers."""
    large_numbers = [
        2**32,
        2**48,
        2**63 - 1,  # Max u64
        999999999999999999,
        1234567890123456789,
    ]

    for num in large_numbers:
        encoded = b62.encode(num)
        decoded = b62.decode(encoded)
        assert decoded == num


def test_consistent_encoding():
    """Test that encoding is consistent and deterministic."""
    test_num = 123456789
    encoded1 = b62.encode(test_num)
    encoded2 = b62.encode(test_num)
    assert encoded1 == encoded2
    assert encoded1 == "8M0kX"  # Known value


def test_leading_zeros():
    """Test that encoding doesn't produce leading zeros."""
    # Base62 encoding should never produce leading zeros
    # except for the number 0 itself
    for i in range(1, 1000):
        encoded = b62.encode(i)
        assert not encoded.startswith("0") or encoded == "0"


def test_case_sensitivity():
    """Test that decoding is case-sensitive."""
    # Different cases should decode to different values
    assert b62.decode("a") != b62.decode("A")
    assert b62.decode("z") != b62.decode("Z")

    # Verify specific values
    assert b62.decode("a") == 36
    assert b62.decode("A") == 10
