# b62

![PyPI version](https://img.shields.io/pypi/v/b62.svg)
![Python Version](https://img.shields.io/pypi/pyversions/b62.svg)
![Total downloads](https://static.pepy.tech/badge/b62)
![License](https://img.shields.io/pypi/l/b62.svg)
![Build Status](https://github.com/smirnoffmg/b62/actions/workflows/ci.yml/badge.svg)

*Because the world desperately needed another Base62 library.*

## What 🤔

Converts integers to strings and back. Revolutionary stuff.

- Uses Rust 🦀 (because Python is apparently too slow for basic arithmetic)
- Zero dependencies (we're very proud of this achievement)
- Type hints (for people who forgot what integers look like)

## Install

```bash
pip install b62
```

*Shocking, we know.*

## Usage

```python
import b62

# Turn number into string
encoded = b62.encode(123456789)  # "8M0kX"

# Turn string back into number  
decoded = b62.decode("8M0kX")    # 123456789

# It throws errors when you give it garbage
try:
    b62.decode("not_base62!")
except ValueError:
    print("Surprise! Invalid input breaks things.")
```

## Batch Operations

For when you have *many* numbers to convert:

```python
# Encode multiple integers (in parallel, because waiting is hard)
encoded = b62.encode_batch([1, 62, 123456789])  # ['1', '10', '8M0kX']

# Decode multiple strings (also in parallel)
decoded = b62.decode_batch(['1', '10', '8M0kX'])  # [1, 62, 123456789]
```

## Performance ⚡

It's fast. Here are some numbers to make you feel better about your life choices:

- **Decode**: ~52ns per operation (congratulations, you saved nanoseconds)
- **Encode**: ~90ns per operation (your URL shortener will thank you)
- **Batch operations**: Uses all your CPU cores (because why not)

*Benchmarks run on a machine that probably costs more than your car.* 💸

## API

### `encode(num: int) -> str`
Converts integer to Base62 string. Rocket science.

### `decode(string: str) -> int` 
Converts Base62 string back to integer. PhD not required.

### `encode_batch(nums: list[int]) -> list[str]`
Like `encode()` but for people with lists.

### `decode_batch(strings: list[str]) -> list[int]`
Like `decode()` but for people with more lists.

## Character Set

```
0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
```

*Yes, we counted. There are 62 of them.*

## Use Cases

- URL shortening (because long URLs hurt feelings)
- Database ID obfuscation (security through obscurity, naturally)
- Compact serialization (for when JSON is "too verbose")
- Impressing coworkers with Rust integration

## Development

```bash
make test    # Run tests (they probably pass)
make ci      # Pretend you care about CI
make build   # Build the thing
```

## License

MIT - Because we're not monsters. 😇

---

*Now go forth and encode responsibly.*