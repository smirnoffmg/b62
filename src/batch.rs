use pyo3::prelude::*;

// Import the encode/decode logic from lib.rs
use super::{to_base62, from_base62};
use rayon::prelude::*;

/// Batch encode a list of u64 numbers to Base62 strings (parallelized)
#[pyfunction]
pub fn encode_batch(nums: Vec<u64>) -> PyResult<Vec<String>> {
    Ok(nums.into_par_iter().map(to_base62).collect())
}

/// Batch decode a list of Base62 strings to u64 numbers (parallelized)
#[pyfunction]
pub fn decode_batch(strs: Vec<String>) -> PyResult<Vec<u64>> {
    strs.into_par_iter()
        .map(|s| {
            from_base62(&s).ok_or_else(|| {
                pyo3::exceptions::PyValueError::new_err(format!("Invalid Base62 string: {}", s))
            })
        })
        .collect()
}

// SIMD prototype: for now, just a batch version. Real SIMD would use packed_simd or std::simd for parallelism.
