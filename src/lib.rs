use pyo3::prelude::*;


const BASE62_CHARS: &[u8; 62] = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

fn to_base62(mut num: u64) -> String {
    if num == 0 {
        return "0".to_string();
    }

    let mut result = Vec::new();
    while num > 0 {
        let rem = (num % 62) as usize;
        result.push(BASE62_CHARS[rem]);
        num /= 62;
    }
    result.reverse();
    String::from_utf8(result).unwrap()
}

fn from_base62(s: &str) -> Option<u64> {
    let mut num: u64 = 0;
    for c in s.bytes() {
        num = num.checked_mul(62)?;
        let val = match c {
            b'0'..=b'9' => (c - b'0') as u64,
            b'A'..=b'Z' => (c - b'A' + 10) as u64,
            b'a'..=b'z' => (c - b'a' + 36) as u64,
            _ => return None, // invalid character
        };
        num = num.checked_add(val)?;
    }
    Some(num)
}

#[pyfunction]
fn encode(num: u64) -> PyResult<String> {
    Ok(to_base62(num))
}

#[pyfunction]
fn decode(s: &str) -> PyResult<u64> {
    from_base62(s).ok_or_else(|| pyo3::exceptions::PyValueError::new_err("Invalid Base62 string"))
}

#[pymodule]
fn b62(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(encode, m)?)?;
    m.add_function(wrap_pyfunction!(decode, m)?)?;
    Ok(())
}
