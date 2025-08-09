# Create a graph with a single node that takes list of numbers and symbol (+/*) and returns the result

import math

from typing import TypedDict, Union, Literal
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    name: str
    numbers: list[int]
    symbol: Union[Literal['+'], Literal['*']]
    result: str


def calculate_result(state: AgentState) -> AgentState:
    """Calculates the result of the numbers based on the symbol."""
    if state['symbol'] == '+':
        state['result'] = f"Hey {state['name']}, The sum of {state['numbers']} is {sum(state['numbers'])}"
    elif state['symbol'] == '*':
        state['result'] = f"Hey {state['name']}, The product of {state['numbers']} is {math.prod(state['numbers'])}"
    return state


graph = StateGraph(AgentState)

graph.add_node("calculate_result", calculate_result)

graph.set_entry_point("calculate_result")
graph.set_finish_point("calculate_result")

app = graph.compile()

result_sum = app.invoke({"name": "John", "numbers": [1, 2, 3, 4], "symbol": "+"})

result_prod = app.invoke({"name": "John", "numbers": [1, 2, 3, 4], "symbol": "*"})

print(result_sum["result"])
print(result_prod["result"])
