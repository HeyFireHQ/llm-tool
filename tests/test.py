#!/usr/bin/env python3

import unittest
from typing import Dict, List, Union, Tuple

from llm_tool import tool, GlobalToolConfig, DocStringException, DefinedFunction, get_type_name, TypeParsingException

class TestTool(unittest.TestCase):

    def test_best_case(self):
        @tool()
        def test(a: str, b: int, c: Dict[str, str], d: List[str], e: bool, f: float, g: List[Dict[str, str]], h: Union[bool, None], i: Union[Dict[str, str], None] = None) -> Dict:
            """
            This is a test function.
            :param a: this is the description for a
            :param b: this is the description for b
            :param c: this is the description for c
            :param d: this is the description for d
            :param e: this is the description for e
            :param f: this is the description for f
            :param g: this is the description for g
            :param h: this is the description for h

            :return: this is the description for return
            """
            pass

            self.assertEqual(test.definition, {
                'type': 'function',
                'function': {
                    'name': 'test',
                    'description': 'This is a test function.\n\nReturn Type: Dict\n\nReturns: this is the description for reteurn',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'a': {
                                'type': 'str',
                                'description': 'this is the description for a',
                            },
                            'b': {
                                'type': 'int',
                                'description': 'this is the description for b',
                            },
                            'c': {
                                'type': 'Dict',
                                'description': 'this is the description for c',
                            },
                            'd': {
                                'type': 'List',
                                'description': 'this is the description for d. Defaults to ["1", "2", "3"]',
                            },
                            'e': {
                                'type': 'bool',
                                'description': 'this is the description for e',
                            },
                            'f': {
                                'type': 'float',
                                'description': 'this is the description for f',
                            },
                            'g': {
                                'type': 'List',
                                'description': 'this is the description for g',
                            },
                            'h': {
                                'type': 'Union',
                                'description': 'this is the description for h',
                            },
                            'i': {
                                'type': 'Union',
                                'description': 'this is the description for i. Defaults to None',
                            },

                        },
                        'required': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
                    }
                }
            })

    def test_default_val_in_desc(self):
        @tool()
        def test(a: str = "test") -> None:
            pass

        self.assertTrue("Default Value: `test`" in test.definition['function']['parameters']['properties']['a']['description'])

    def test_param_type_exception(self):
        def test(a: str, b) -> None:
            pass

        with self.assertRaisesRegex(DocStringException, "No type found for parameter `[a-zA-Z\d_]*` in function `[a-zA-Z\d_]*`"):
            tool()(test)

    def test_param_desc_exception(self):
        def test(a: str) -> None:
           pass

        with self.assertRaisesRegex(DocStringException, "Parameter `[a-zA-Z\d_]*` description not found in docstring of `[a-zA-Z\d_]*` function signature."):
            tool(desc_required=True)(test)

    def test_return_type_required_exception(self):
        def test(a: str):
            """
            :return: this is a return description
            """
            pass

        with self.assertRaisesRegex(DocStringException, "Return type not found in function `[a-zA-Z\d_]*`."):
            tool(return_required=True)(test)

    def test_return_desc_required_exception(self):
        def test(a: str) -> int:
            pass

        with  self.assertRaisesRegex(DocStringException, "Return description not found in docstring of `[a-zA-Z\d_]*` function signature."):
            tool(return_required=True)(test)

class TestDefinedFunction(unittest.TestCase):
    
    def test_call(self):
        def test(a: int, b: int) -> List[int]:
            return [a, b]

        definedFunction = DefinedFunction(test)
        self.assertEqual(definedFunction(1, b=2), [1, 2])

class TestGlobalToolConfig(unittest.TestCase):
    def test_default(self):
        self.assertEqual(GlobalToolConfig.desc_required, False)
        self.assertEqual(GlobalToolConfig.return_required, False)

class TestGetTypeName(unittest.TestCase):
    def test_primitives(self):
        self.assertEqual(get_type_name(int), "int")
        self.assertEqual(get_type_name(str), "str")
        self.assertEqual(get_type_name(float), "float")
        self.assertEqual(get_type_name(bool), "bool")

    def test_typing_types(self):
        self.assertEqual(get_type_name(List), "List")
        self.assertEqual(get_type_name(Dict), "Dict")
        self.assertEqual(get_type_name(Union), "Union")
        self.assertEqual(get_type_name(Tuple), "Tuple")

    def test_none(self):
        self.assertEqual(get_type_name(None), "None")

    def test_type_parsing_exception(self):
        with self.assertRaisesRegex(TypeParsingException, "Failed to parse type: 1"):
            get_type_name(1)

if __name__ == '__main__':
    unittest.main()

