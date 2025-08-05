from hypothesis import given
from hypothesis import strategies as st

import b62


@given(st.integers(min_value=0, max_value=2**63 - 1))
def test_hypothesis_encode_decode_roundtrip(num):
    encoded = b62.encode(num)
    decoded = b62.decode(encoded)
    assert decoded == num
