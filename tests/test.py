#!/usr/bin/env python3

from llm_tool import tool, GlobalToolConfig
from llm_tool.llm_tool import parse_docstring

from typing import List

GlobalToolConfig.return_required = True
GlobalToolConfig.desc_required = True

hay = """
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

a = parse_docstring(hay)
# print(a.returns)
# print(a.description)
# print(a.params)

@tool(desc_required=False)
def test_func(graph_data: List[float], portfolio_name: str, description: str = "This is a description", marketValue: float = 14_000) -> None:
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
    print(graph_data)
    print(portfolio_name)
    print(description)
    print(marketValue)

# call test_func
# test_func([1, 2, 3, 4], "test", "test", 10)
#
print(test_func.definition)
