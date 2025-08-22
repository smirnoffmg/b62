# b62

![PyPI version](https://img.shields.io/pypi/v/b62.svg)
![Python Version](https://img.shields.io/pypi/pyversions/b62.svg)
![Total downloads](https://static.pepy.tech/badge/b62)
![License](https://img.shields.io/pypi/l/b62.svg)
![Build Status](https://github.com/smirnoffmg/b62/actions/workflows/ci.yml/badge.svg)

🎉 A lightning-fast, zero-dependency and friendly Base62 encoder/decoder for Python! Tame your data with style and a smile.

## Features

- ⚡ High-performance Base62 encode/decode for integers
- 🐍 Friendly Python interface backed by Rust
- 🔧 Seamless Rust-Python integration via PyO3
- 🛡️ Type-safe with comprehensive error handling
- 🧪 Thoroughly tested with property-based testing
- 📦 Zero runtime dependencies

## Installation

### From PyPI

```bash
pip install b62
```

## Usage


```python
import b62

# Encode an integer to Base62
encoded = b62.encode(123456789)
print(encoded)  # Output: "8M0kX"

# Decode a Base62 string back to integer
decoded = b62.decode("8M0kX")
print(decoded)  # Output: 123456789

# Error handling
try:
    b62.decode("invalid!")
except ValueError as e:
    print(f"Invalid Base62 string: {e}")

# Round-trip validation
original = 987654321
encoded = b62.encode(original)
decoded = b62.decode(encoded)
assert original == decoded  # Always True!
```

## Performance

b62 is built with Rust for maximum performance and delivers exceptional speed:



### Benchmark Results

**Single Operations (nanoseconds per operation):**

- **Decode single large string**: ~52ns (19,300 Kops/sec)
- **Encode single large number**: ~90ns (11,100 Kops/sec)
- **Decode edge cases**: ~190ns (5,270 Kops/sec)
- **Encode edge cases**: ~408ns (2,450 Kops/sec)
- **Decode small numbers**: ~26,500ns (37.7 Kops/sec)
- **Encode small numbers**: ~59,300ns (16.9 Kops/sec)

**Batch Operations (parallel, per operation):**

- **Batch decode small numbers**: ~44,000ns (22.7 Kops/sec)
- **Batch encode small numbers**: ~49,500ns (20.2 Kops/sec)
- **Batch decode large numbers**: ~848ns (1,180 Kops/sec)
- **Batch encode large numbers**: ~1,059ns (944 Kops/sec)
- **Batch decode mixed numbers**: ~749ns (1,335 Kops/sec)
- **Batch encode mixed numbers**: ~885ns (1,130 Kops/sec)

**Performance Characteristics:**

- **Batch operations**: Use all CPU cores for maximum throughput (parallelized with Rayon)
- **Encoding/Decoding**: Much faster than pure Python implementations
- **Memory**: Minimal memory footprint with zero allocations for small numbers
- **CPU**: Optimized for both small and large integers
- **Scalability**: Consistent performance across number ranges (0 to 2^63-1)

### Technical Implementation

The library uses a highly optimized Rust implementation with PyO3 bindings:

- **Character Set**: `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`
- **Algorithm**: Efficient division/modulo operations with pre-allocated buffers
- **Error Handling**: Comprehensive validation with detailed error messages
- **Type Safety**: Full type annotations and runtime validation
- **Memory Management**: Zero-copy operations where possible


## Batch Operations

For high-throughput scenarios, b62 provides batch operations that leverage parallel processing for maximum speed:

### `b62.encode_batch(nums: list[int]) -> list[str]`
Encodes a list of integers to Base62 strings in parallel.

**Parameters:**

- `nums` (list[int]): List of integers to encode (must be non-negative)

**Returns:**
- `list[str]`: List of Base62 encoded strings

**Raises:**
- `OverflowError`: If any integer is too large for u64

**Example:**
```python
import b62
numbers = [1, 62, 123456789]
encoded = b62.encode_batch(numbers)
print(encoded)  # Output: ['1', '10', '8M0kX']
```

### `b62.decode_batch(strings: list[str]) -> list[int]`
Decodes a list of Base62 strings back to integers in parallel.

**Parameters:**
- `strings` (list[str]): List of Base62 strings to decode

**Returns:**
- `list[int]`: List of decoded integers

**Raises:**
- `ValueError`: If any string contains invalid Base62 characters

**Example:**
```python
import b62
strings = ['1', '10', '8M0kX']
decoded = b62.decode_batch(strings)
print(decoded)  # Output: [1, 62, 123456789]
```

**Performance Note:**
Batch operations are highly optimized and use all available CPU cores for parallel processing, making them ideal for large datasets or performance-critical applications.

---

## Development

### Running Tests

```bash
make test
```

### Code Quality

```bash
make ci
```

### Building

```bash
make build_package
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass before submitting

## License

MIT License - free and open for all! 🎉

## Why b62?

Keep your integer conversions speedy and stylish! Perfect for:

- URL shortening
- Database ID encoding
- Compact data serialization
- Performance-critical applications

🦀🐍💨
