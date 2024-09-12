
use pyo3::prelude::*;
use regex::Regex;
use std::collections::HashMap;

#[derive(Debug)]
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

    #[test]
    fn test_empty_string() {
        let docstring = "";
        let parsed_docstring = parse_docstring(docstring);
        assert_eq!(parsed_docstring.description, "");
        assert_eq!(parsed_docstring.returns, "");
        assert_eq!(parsed_docstring.params, HashMap::new());
    }

    #[test]
    fn test_normal_string() {
        let docstring = "
        This is a description
        :param x: This is the description of x
        :param y: This is the description of y
        :return: This is the return description
        ";
        let parsed_docstring = parse_docstring(docstring);
        assert_eq!(parsed_docstring.description, String::from("This is a description"));
        assert_eq!(parsed_docstring.returns, String::from("This is the return description"));
        assert_eq!(parsed_docstring.params, HashMap::from([(String::from("x"), String::from("This is the description of x")), (String::from("y"), String::from("This is the description of y"))]));
    }

    #[test]
    fn test_no_description() {
        let docstring = "
        :param x: This is the description of x
        :param y: This is the description of y
        :return: This is the return description
        ";
        let parsed_docstring = parse_docstring(docstring);
        assert_eq!(parsed_docstring.description, String::from(""));
        assert_eq!(parsed_docstring.returns, String::from("This is the return description"));
        assert_eq!(parsed_docstring.params, HashMap::from([(String::from("x"), String::from("This is the description of x")), (String::from("y"), String::from("This is the description of y"))]));
    }
    
    #[test]
    fn test_no_params() {
        let docstring = "
        This is a description
        :return: This is the return description
        ";
        let parsed_docstring = parse_docstring(docstring);
        assert_eq!(parsed_docstring.description, String::from("This is a description"));
        assert_eq!(parsed_docstring.returns, String::from("This is the return description"));
        assert_eq!(parsed_docstring.params, HashMap::new());
    }

    #[test]
    fn test_no_return() {
        let docstring = "
        This is a description
        :param x: This is the description of x
        :param y: This is the description of y
        ";
        let parsed_docstring = parse_docstring(docstring);
        assert_eq!(parsed_docstring.description, String::from("This is a description"));
        assert_eq!(parsed_docstring.returns, String::from(""));
        assert_eq!(parsed_docstring.params, HashMap::from([(String::from("x"), String::from("This is the description of x")), (String::from("y"), String::from("This is the description of y"))]));
    }

    #[test]
    fn test_no_param_description() {
        let docstring = "
        This is a description
        :param x:
        :param y:
        :param z: This is the description of z
        :return: This is the return description
        ";
        let parsed_docstring = parse_docstring(docstring);
        assert_eq!(parsed_docstring.description, String::from("This is a description"));
        assert_eq!(parsed_docstring.returns, String::from("This is the return description"));
        assert_eq!(parsed_docstring.params, HashMap::from([(String::from("x"), String::from("")), (String::from("y"), String::from("")), (String::from("z"), String::from("This is the description of z"))]));
    }

    #[test]
    fn test_no_return_description() {
        let docstring = "
        This is a description
        :param x: This is the description of x
        :param y: This is the description of y
        :return:
        ";
        let parsed_docstring = parse_docstring(docstring);
        assert_eq!(parsed_docstring.description, String::from("This is a description"));
        assert_eq!(parsed_docstring.returns, String::from(""));
        assert_eq!(parsed_docstring.params, HashMap::from([(String::from("x"), String::from("This is the description of x")), (String::from("y"), String::from("This is the description of y"))]));
    }

    #[test]
    fn test_no_param_name() {
        let docstring = "
        This is a description
        :param : This is the description of x
        :param y: This is the description of y
        :return: This is the return description
        ";
        let parsed_docstring = parse_docstring(docstring);
        assert_eq!(parsed_docstring.description, String::from("This is a description"));
        assert_eq!(parsed_docstring.returns, String::from("This is the return description"));
        assert_eq!(parsed_docstring.params, HashMap::from([(String::from(""), String::from("This is the description of x")), (String::from("y"), String::from("This is the description of y"))]));
    }

    #[test]
    fn test_mispelled_return() {
        let docstring = "
        This is a description
        :param x: this is the description of x
        :retrun: This is the return description
        ";
        let parse_docstring = parse_docstring(docstring);
        assert_eq!(parse_docstring.returns, String::from(""));
    }

    #[test]
    fn test_weird_colons() {
        let docstring = "
        This is a description
        :param x: This is the d:escriptio:n of x
        :param y: This is :the description of y
        :return: This is the return description
        ";
        let parsed_docstring = parse_docstring(docstring);
        assert_eq!(parsed_docstring.description, String::from("This is a description"));
        assert_eq!(parsed_docstring.returns, String::from("This is the return description"));
        assert_eq!(parsed_docstring.params, HashMap::from([(String::from("x"), String::from("This is the d")), (String::from("y"), String::from("This is"))]));
    }
}
