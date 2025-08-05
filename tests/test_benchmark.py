"""
Performance benchmarks for b62 library using pytest-benchmark.
"""

import pytest

import b62


@pytest.mark.benchmark
def test_encode_small_numbers(benchmark):
    """Benchmark encoding small numbers (0-999)."""
    numbers = list(range(1000))

    def encode_numbers():
        return [b62.encode(n) for n in numbers]

    result = benchmark(encode_numbers)
    assert len(result) == 1000
    assert result[0] == "0"
    assert result[61] == "z"
    assert result[62] == "10"


@pytest.mark.benchmark
def test_decode_small_numbers(benchmark):
    """Benchmark decoding small numbers."""
    strings = [b62.encode(n) for n in range(1000)]

    def decode_strings():
        return [b62.decode(s) for s in strings]

    result = benchmark(decode_strings)
    assert len(result) == 1000
    assert result[0] == 0
    assert result[61] == 61
    assert result[62] == 62


@pytest.mark.benchmark
def test_encode_large_numbers(benchmark):
    """Benchmark encoding large numbers."""
    numbers = [2**i for i in range(10, 64, 4)]  # Powers of 2

    def encode_large():
        return [b62.encode(n) for n in numbers]

    result = benchmark(encode_large)
    assert len(result) == len(numbers)


@pytest.mark.benchmark
def test_decode_large_numbers(benchmark):
    """Benchmark decoding large numbers."""
    numbers = [2**i for i in range(10, 64, 4)]
    strings = [b62.encode(n) for n in numbers]

    def decode_large():
        return [b62.decode(s) for s in strings]

    result = benchmark(decode_large)
    assert len(result) == len(numbers)
    assert result == numbers


@pytest.mark.benchmark
def test_encode_mixed_numbers(benchmark):
    """Benchmark encoding mixed number sizes."""
    numbers = [
        0,
        1,
        10,
        61,
        62,
        123,
        1000,
        10000,
        100000,
        1000000,
        2**16,
        2**32,
        2**48,
        2**63 - 1,
    ]

    def encode_mixed():
        return [b62.encode(n) for n in numbers]

    result = benchmark(encode_mixed)
    assert len(result) == len(numbers)


@pytest.mark.benchmark
def test_decode_mixed_numbers(benchmark):
    """Benchmark decoding mixed number sizes."""
    numbers = [
        0,
        1,
        10,
        61,
        62,
        123,
        1000,
        10000,
        100000,
        1000000,
        2**16,
        2**32,
        2**48,
        2**63 - 1,
    ]
    strings = [b62.encode(n) for n in numbers]

    def decode_mixed():
        return [b62.decode(s) for s in strings]

    result = benchmark(decode_mixed)
    assert len(result) == len(numbers)
    assert result == numbers


@pytest.mark.benchmark
def test_roundtrip_performance(benchmark):
    """Benchmark round-trip encode/decode performance."""
    numbers = list(range(1000))

    def roundtrip():
        results = []
        for num in numbers:
            encoded = b62.encode(num)
            decoded = b62.decode(encoded)
            results.append(decoded)
        return results

    result = benchmark(roundtrip)
    assert len(result) == 1000
    assert result == numbers


@pytest.mark.benchmark
def test_encode_single_large_number(benchmark):
    """Benchmark encoding a single large number."""
    large_num = 2**63 - 1

    def encode_single():
        return b62.encode(large_num)

    result = benchmark(encode_single)
    assert result == "AzL8n0Y58m7"


@pytest.mark.benchmark
def test_decode_single_large_string(benchmark):
    """Benchmark decoding a single large string."""
    large_string = "AzL8n0Y58m7"

    def decode_single():
        return b62.decode(large_string)

    result = benchmark(decode_single)
    assert result == 2**63 - 1


@pytest.mark.benchmark
def test_encode_edge_cases(benchmark):
    """Benchmark encoding edge cases."""
    edge_cases = [0, 1, 61, 62, 62**2, 62**3]

    def encode_edges():
        return [b62.encode(n) for n in edge_cases]

    result = benchmark(encode_edges)
    expected = ["0", "1", "z", "10", "100", "1000"]
    assert result == expected


@pytest.mark.benchmark
def test_decode_edge_cases(benchmark):
    """Benchmark decoding edge cases."""
    edge_strings = ["0", "1", "z", "10", "100", "1000"]

    def decode_edges():
        return [b62.decode(s) for s in edge_strings]

    result = benchmark(decode_edges)
    expected = [0, 1, 61, 62, 62**2, 62**3]
    assert result == expected
