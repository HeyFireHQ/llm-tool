#!/usr/bin/env python3

import unittest
from typing import Dict, List, Union

from llm_tool import tool, GlobalToolConfig, DocStringException, TypeParsingException

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

        with self.assertRaisesRegex(DocStringException, "No type found for parameter `[a-zA-Z_]*` in function `[a-zA-Z_]*`"):
            tool()(test)

    def test_param_desc_exception(self):
        def test(a: str) -> None:
           pass

        with self.assertRaisesRegex(DocStringException, "Parameter `[a-zA-Z_]*` description not found in docstring of `[a-zA-Z_]*` function signature."):
            tool(desc_required=True)(test)

    def test_return_type_required_exception(self):
        def test(a: str):
            """
            :return: this is a return description
            """
            pass

        with self.assertRaisesRegex(DocStringException, "Return type not found in function `[a-zA-Z_]*`."):
            tool(return_required=True)(test)

    def test_return_desc_required_exception(self):
        def test(a: str) -> int:
            pass

        with  self.assertRaisesRegex(DocStringException, "Return description not found in docstring of `[a-zA-Z_]*` function signature."):
            tool(return_required=True)(test)

if __name__ == '__main__':
    unittest.main()

