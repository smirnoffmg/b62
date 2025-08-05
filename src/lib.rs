use pyo3::prelude::*;

/// Base62 encode an integer
#[pyfunction]
fn encode(num: u64) -> PyResult<String> {
    // Dummy example for illustration
    Ok(format!("base62({})", num))
}

/// Base62 decode a string to integer
#[pyfunction]
fn decode(s: &str) -> PyResult<u64> {
    // Dummy example for illustration
    Ok(s.len() as u64)
}

#[pymodule]
fn b62(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(encode, m)?)?;
    m.add_function(wrap_pyfunction!(decode, m)?)?;
    Ok(())
}
