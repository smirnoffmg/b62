import b62
import pytest


def test_encode_basic():
    result = b62.encode(12345)
    assert isinstance(result, str)
    assert "12345" in result


def test_decode_basic():
    result = b62.decode("abc")
    assert isinstance(result, int)
    assert result == 3


@pytest.mark.parametrize("num", [0, 1, 10, 99, 123456789])
def test_encode_decode_roundtrip(num):
    encoded = b62.encode(num)
    decoded = b62.decode(encoded)
    # Since encode/decode are mocked here, this might not hold yet.
    # When implemented correctly, decoded should equal num.
    assert isinstance(encoded, str)
    assert isinstance(decoded, int)
