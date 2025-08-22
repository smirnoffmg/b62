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

def encode_batch(nums: list[int]) -> list[str]:
    """
    Encode a list of integers to Base62 string representations in parallel.

    Args:
        nums: List of integers to encode (must be non-negative)

    Returns:
        List of Base62 encoded strings

    Raises:
        OverflowError: If any integer is too large for u64
    """
    ...

def decode_batch(strings: list[str]) -> list[int]:
    """
    Decode a list of Base62 strings back to integers in parallel.

    Args:
        strings: List of Base62 strings to decode

    Returns:
        List of decoded integers

    Raises:
        ValueError: If any string contains invalid Base62 characters
    """
    ...
