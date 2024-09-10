
use pyo3::prelude::*;
use regex::Regex;
use std::collections::HashMap;

#[pyclass]
pub struct ParsedDocstring {
    #[pyo3(get, set)]
    description: String,
    #[pyo3(get, set)]
    returns: String,
    #[pyo3(get, set)]
    params: HashMap<String, String>,
}

#[pyfunction]
pub fn parse_docstring(docstring: &str) -> ParsedDocstring {

    let desc_re = Regex::new(r"([^:]*)").unwrap();
    let param_re = Regex::new(r"(?::param (?<name>[A-Za-z_]*):(?<desc>[^:]*))").unwrap();
    let return_re = Regex::new(r"(?::return\w*:(?<desc>[^:]*))").unwrap();
  
    let description: String = String::from(desc_re.captures(docstring).unwrap()[0].trim());
    
    let mut params = HashMap::new();
    for cap in param_re.captures_iter(docstring) {
        let name = cap.name("name").unwrap().as_str();
        let desc = cap.name("desc").unwrap().as_str().trim();
        params.insert(String::from(name), String::from(desc));
    }

    let returns: String = String::from(match return_re.captures(docstring) {
        Some(cap) => cap.name("desc").unwrap().as_str().trim(),
        None => "",
    });

    ParsedDocstring {
        description, 
        returns,
        params,
    }

}

/// A Python module implemented in Rust.
#[pymodule]
fn llm_tool(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_docstring, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
}
