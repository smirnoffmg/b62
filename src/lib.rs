use pyo3::prelude::*;
mod batch;

const BASE62_CHARS: &[u8; 62] = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
const MAX_BASE62_LENGTH: usize = 13; // Maximum length for u64 in Base62 is 13

/// Convert a u64 number to Base62 string representation.
///
/// # Arguments
///
/// * `num` - The number to convert to Base62
///
/// # Returns
///
/// A Base62 string representation of the number
///
/// # Panics
///
/// This function may panic if the UTF-8 conversion of the result fails.
/// This should not happen with valid Base62 character encoding.
fn to_base62(mut num: u64) -> String {
    if num == 0 {
        return "0".to_string();
    }

    let mut result = [0u8; MAX_BASE62_LENGTH];
    let mut index = MAX_BASE62_LENGTH;

    while num > 0 {
        let rem = (num % 62) as usize;
        index -= 1;
        result[index] = BASE62_CHARS[rem];
        num /= 62;
    }

    // Convert the relevant part of the array to a string
    String::from_utf8(result[index..].to_vec()).unwrap()
}

fn from_base62(s: &str) -> Option<u64> {
    if s.is_empty() {
        return None;
    }

    let mut num: u64 = 0;
    for c in s.bytes() {
        num = num.checked_mul(62)?;
        let val = match c {
            b'0'..=b'9' => u64::from(c - b'0'),
            b'A'..=b'Z' => u64::from(c - b'A' + 10),
            b'a'..=b'z' => u64::from(c - b'a' + 36),
            _ => return None, // invalid character
        };
        num = num.checked_add(val)?;
    }
    Some(num)
}

/// Encode a u64 number to Base62 string (Python binding).
///
/// # Arguments
///
/// * `num` - The number to encode
///
/// # Returns
///
/// A Base62 string representation of the number
///
/// # Errors
///
/// This function does not return errors as the conversion is infallible.
#[pyfunction]
#[allow(clippy::unnecessary_wraps)]
fn encode(num: u64) -> PyResult<String> {
    Ok(to_base62(num))
}

/// Decode a Base62 string to u64 number (Python binding).
///
/// # Arguments
///
/// * `s` - The Base62 string to decode
///
/// # Returns
///
/// The decoded u64 number
///
/// # Errors
///
/// Returns a `PyValueError` if the string is empty or contains invalid characters.
#[pyfunction]
fn decode(s: &str) -> PyResult<u64> {
    if s.is_empty() {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "Empty string cannot be decoded",
        ));
    }

    from_base62(s).ok_or_else(|| {
        // Provide more specific error messages
        let invalid_chars: Vec<char> = s.chars().filter(|&c| !c.is_alphanumeric()).collect();
        if invalid_chars.is_empty() {
            pyo3::exceptions::PyValueError::new_err(format!("Invalid Base62 string: '{s}'"))
        } else {
            pyo3::exceptions::PyValueError::new_err(format!(
                "Invalid characters in Base62 string: '{}'",
                invalid_chars.iter().collect::<String>()
            ))
        }
    })
}

/// Initialize the b62 Python module.
///
/// # Arguments
///
/// * `_py` - Python interpreter instance
/// * `m` - Module to add functions to
///
/// # Returns
///
/// Success or failure of module initialization
///
/// # Errors
///
/// Returns a `PyErr` if module initialization fails.
#[pymodule]
fn b62(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(encode, m)?)?;
    m.add_function(wrap_pyfunction!(decode, m)?)?;
    m.add_function(wrap_pyfunction!(batch::encode_batch, m)?)?;
    m.add_function(wrap_pyfunction!(batch::decode_batch, m)?)?;
    // Add module docstring
    m.add(
        "__doc__",
        "High-performance Base62 encoder/decoder for Python",
    )?;
    Ok(())
}
