use pyo3::prelude::*;

// Import the encode/decode logic from lib.rs
use super::{from_base62, to_base62};
use rayon::prelude::*;

const MAX_BATCH_SIZE: usize = 1_000_000; // Prevent memory exhaustion

/// Batch encode a list of u64 numbers to Base62 strings (parallelized)
#[pyfunction]
pub fn encode_batch(nums: Vec<u64>) -> PyResult<Vec<String>> {
    // Input validation
    if nums.is_empty() {
        return Ok(vec![]);
    }
    if nums.len() > MAX_BATCH_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Batch size too large: {} (max: {})",
            nums.len(),
            MAX_BATCH_SIZE
        )));
    }

    Ok(nums.into_par_iter().map(to_base62).collect())
}

/// Batch decode a list of Base62 strings to u64 numbers (parallelized)
#[pyfunction]
pub fn decode_batch(strs: Vec<String>) -> PyResult<Vec<u64>> {
    // Input validation
    if strs.is_empty() {
        return Ok(vec![]);
    }
    if strs.len() > MAX_BATCH_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Batch size too large: {} (max: {})",
            strs.len(),
            MAX_BATCH_SIZE
        )));
    }

    strs.into_par_iter()
        .enumerate()
        .map(|(index, s)| {
            from_base62(&s).ok_or_else(|| {
                pyo3::exceptions::PyValueError::new_err(format!(
                    "Invalid Base62 string at index {}: '{}'",
                    index, s
                ))
            })
        })
        .collect()
}

// SIMD prototype: for now, just a batch version. Real SIMD would use packed_simd or std::simd for parallelism.
