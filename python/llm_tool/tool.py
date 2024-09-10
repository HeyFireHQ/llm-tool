from llm_tool import llm_tool

import inspect
from typing import Callable, Union, _BaseGenericAlias

def tool(func: Callable) -> Callable:
    parsed = None
    if func.__doc__:
        parsed = llm_tool.parse_docstring(func.__doc__)

    params = {
        "type": "object",
        "properties": {}
    }

    if inspect.signature(func)._parameters:
        # ignore error
        for key, value in inspect.signature(func)._parameters.items():
            
            param_type: Union[type, _BaseGenericAlias] = value.annotation
            is_required: bool = value._default is inspect._empty 

            try:
                params["properties"][key] = {
                    "type": param_type._name if isinstance(param_type, _BaseGenericAlias) else param_type.__name__,
                    "description": parsed.params.get(key, "") if parsed else ""
                }
            except KeyError:
                raise Exception(f"Parameter mismatch between doc and function signature.\nFound `{key}` in docstring but not in function signature.")

            # add required parameters
            if not isinstance(params.get("required", None), list): params["required"] = [] 
            if is_required: params["required"].append(key)

    else:
        params = {}

    out = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": parsed.description if parsed else "",
            "parameters": params,
        }
    }

    return func
