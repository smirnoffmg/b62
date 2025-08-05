"""
Type stubs for b62 module.

This module provides high-performance Base62 encoding and decoding functionality.
"""

def encode(num: int) -> str:
    """
    Encode an integer to Base62 string representation.

    Args:
        num: Integer to encode (must be non-negative)

    Returns:
        Base62 encoded string

    Raises:
        OverflowError: If the integer is too large for u64
    """
    ...

def decode(s: str) -> int:
    """
    Decode a Base62 string back to an integer.

    Args:
        s: Base62 string to decode

    Returns:
        Decoded integer

    Raises:
        ValueError: If the string contains invalid Base62 characters
    """
    ...
