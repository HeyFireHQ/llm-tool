#!/usr/bin/env python3

import llm_tool

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

a = llm_tool.parse_docstring(hay)
print(type(a))
print(dir(a))
print(a)

print("Description: ", a.description)
print("Returns: ", a.returns)
print("params: ", a.params)
