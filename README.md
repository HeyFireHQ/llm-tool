# llm-tool
A simple Python module to automatically turn your functions into definitions that can be used for LLM tool calling. Built with Rust for blazing fast string parsing.

## Instalation
```bash
pip install llm-tool
```

## Usage
Just use the `@tool()` decorator to automatically turn a function into a tool definition.

```python
from llm_tool import tool

@tool()
def test_func(graph_data: List[float], portfolio_name: str, description: str = "This is a description", marketValue: float = 14_000) -> List[float]:
    """
    Generate an image with the given data.
    
    :param graph_data: List of data points to be plotted on the graph.
    We only need the y-axis values.
    The x-axis values will be calculated based on the length of the list.
    All values are normalized to fit the graph region.
    
    :param portfolio_name: Name of the portfolio.
    :param description: Description of the portfolio.
    :param marketValue: The marketValue of the portfolio.
    
    :return: Processed Image with the given data drawn.
    """
    pass
```

Get the definition:
```python
definition = test_func.definition
```

You can still use the function:
```python
test_func(...)
```

Definitions are generated based on the format specified by the [Berkeley Function-Calling Benchmark](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html#metrics).
<br />
The definition for the function above will look like this:
```python
{
  'type': 'function',
  'function': {
    'name': 'test_func',
    'description': 'Generate an image with the given data.\n\nReturn Type: `None`\n\nReturn Description: Processed Image with the given data drawn.',
    'parameters': {
      'type': 'object',
      'properties': {
        'graph_data': {
          'type': 'List',
          'description': 'List of data points to be plotted on the graph.\n    We only need the y-axis values.\n
    The x-axis values will be calculated based on the length of the list.\n    All values are normalized to fit the graph region.'
        },
        'portfolio_name': {
          'type': 'str',
          'description': 'Name of the portfolio.'
        },
        'description': {
          'type': 'str',
          'description': 'Description of the portfolio. Default Value: `This is a description`'
        },
        'marketValue': {
            'type': 'float',
            'description': 'The marketValue of the portfolio. Default Value: `14000`'
        }
      },
    'required': ['graph_data', 'portfolio_name']
    }
  }
}
```

### Use with methods
```python
fomr llm_tool import tool

class TestClass:
    
    @tool(self)
    def test_method(self, a: int = 0) -> None:
        '''
        This is a test method.

        :param a: This is a test parameter.
        '''
        pass

# get the definition from the class
definition = TestClass.test_method.definition
# or from an object
t = TestClass()
definition = t.test_method.definition
```

### Groq API Example
```python
from groq import Groq
from llm_tool import tool

client = Groq(api_key=GROQ_KEY)

@tool()
def get_user_data(userId: str) -> Dict[str, str]:
  """
  Fetch user data from database.

  :param userId: The user's id.
  :return: Dictionary with user's data
  """
  pass

@tool()
def create_user(username: str, pass: str, created_at: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) -> None:
  """
  Create a new user

  :param username: user username
  :param pass: user password
  :param create_at: date user was created
  """
  pass

tools = [
  get_user_data.definition,
  create_user.definition,
]

response = client.chat.completions.create(
    messages=messages,
    
    model="llama-3.1-70b-versatile",
    
    tools=tools,
    tool_choice="auto",
)

tool_calls = response.choices[0].message.tool_calls
```

### Scope
The `@tool()` decorator can work for functions with less documentation.
Everything in the documentation and typing of the function is optional except for parameter type hints.

The following will raise a ```DocStringException```:
```python
@tool()
def test(a) -> None:
  pass
```

But all of the following are legal:
```python

# Just a description, no return typing hint or parameter description.
@tool()
def test(a: int):
  """
  This is a description.
  """
  pass

# No docstring
@tool()
def test(a: int):
  pass

# Return Type Hint without return deswcription
@tool()
def test(a: int) -> None:
  pass

# Return description without return type hint
@tool()
def test(a: int):
  """
  :return: test return description
  """
  pass

# Docstring with parameter descriptions and no return description
def test(a: int) -> None:
  """
  Description
  :param a: another description
  """
  pass

# Or any combination of the above
```

### Configuration
The `@tool()` decorator allows for configuration that enforces more rules.

- `desc_required`: if `True` it makes descriptions for all parameters mandatory, raises `DocStringException` otherwise. Default is `False`
- `return_required`: if `True` it makes the return type hint and return description mandatory, raises `DocStringException` otherwise. Deafult is `False`

There are two ways the `@tool()` decorator:
- Individually
```python
@tool(desc_required=True, return_required=False)
def test(a: int) -> int:
  """
  :param a: description
  :return: return description
  """
  pass

@tool(desc_required=False, return_required=False)
def test(a: int) -> int:
  """
  :return: return description
  """
  pass
```
- Globally
```python
from llm_tool import GlobalToolConfig

GlobalToolConfig.desc_required = True
GlobalToolConfig.return_required = True

@tool()
def test(a: int) -> int:
  """
  :param a: description
  :return: return description
  """
  pass

# ignore global config
@tool(desc_required=False, return_required=False)
def test2(a: int) -> None:
  pass
```

### Support
Currently only docstrings in the [reST](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html) format are supported, but support for more doscstring formats will be added in the future.

### Roadmap
<ul><li>- [ ] </li></ul> Add support for Union types
<ul><li>- [ ] </li></ul> Add support for writing subtypes (e.g. `List[int]` instead of just `List`)
<ul><li>- [ ] </li></ul> Support for more doscstring formats

