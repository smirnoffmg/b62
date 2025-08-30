use pyo3::prelude::*;

// Import the encode/decode logic from lib.rs
use super::{from_base62, to_base62};
use rayon::prelude::*;

const MAX_BATCH_SIZE: usize = 1_000_000; // Prevent memory exhaustion

/// Batch encode a list of u64 numbers to Base62 strings (parallelized).
///
/// # Arguments
///
/// * `nums` - Vector of u64 numbers to encode
///
/// # Returns
///
/// Vector of Base62 string representations
///
/// # Errors
///
/// Returns a `PyValueError` if the batch size exceeds the maximum allowed size.
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

/// Batch decode a list of Base62 strings to u64 numbers (parallelized).
///
/// # Arguments
///
/// * `strs` - Vector of Base62 strings to decode
///
/// # Returns
///
/// Vector of decoded u64 numbers
///
/// # Errors
///
/// Returns a `PyValueError` if the batch size exceeds the maximum allowed size
/// or if any string contains invalid Base62 characters.
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

    // Process in parallel but maintain deterministic error reporting
    let mut results = Vec::with_capacity(strs.len());
    let mut first_error = None;

    // Process in parallel and collect results
    let parallel_results: Vec<_> = strs
        .into_par_iter()
        .enumerate()
        .map(|(index, s)| {
            from_base62(&s).ok_or_else(|| {
                pyo3::exceptions::PyValueError::new_err(format!(
                    "Invalid Base62 string at index {index}: '{s}'"
                ))
            })
        })
        .collect();

    // Check results in order and return first error
    for result in parallel_results {
        match result {
            Ok(value) => results.push(value),
            Err(e) => {
                if first_error.is_none() {
                    first_error = Some(e);
                }
                // Continue processing to maintain parallel benefits
            }
        }
    }

    // Return first error if any, otherwise return successful results
    match first_error {
        Some(e) => Err(e),
        None => Ok(results),
    }
}

// SIMD prototype: for now, just a batch version. Real SIMD would use packed_simd or std::simd for parallelism.
