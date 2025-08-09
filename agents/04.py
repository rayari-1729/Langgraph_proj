# conditional edges (2 conditional edges)

from typing import TypedDict, Union, Literal
from langgraph.graph import StateGraph, START, END

from IPython.display import display, Image

class AgentState(TypedDict):
    number1: int
    number2: int
    operation1: Union[Literal['+'], Literal['-']]
    number3: int
    number4: int
    operation2: Union[Literal['+'], Literal['-']]
    result: str

def adder(state: AgentState) -> AgentState:
    """Add the two numbers"""
    state['result'] = f"The sum of {state['number1']} and {state['number2']} is {state['number1'] + state['number2']}"
    return state

def subtractor(state: AgentState) -> AgentState:
    """Subtract the two numbers"""
    state['result'] = f"The difference of {state['number1']} and {state['number2']} is {state['number1'] - state['number2']}"
    return state

def first_router(state: AgentState) -> AgentState:
    """Route the numbers based on the operation"""
    if state['operation1'] == '+':
        return "add_numbers_edge"
    elif state['operation1'] == '-':
        return "subtract_numbers_edge"

def second_router(state: AgentState) -> AgentState:
    """Route the numbers based on the operation"""
    if state['operation2'] == '+':
        return "add_numbers_edge2"
    elif state['operation2'] == '-':
        return "subtract_numbers_edge2"

graph = StateGraph(AgentState)

graph.add_node("add_numbers", adder)
graph.add_node("subtract_numbers", subtractor)
graph.add_node("first_router", lambda state:state)

graph.add_node("add_numbers2", adder)
graph.add_node("subtract_numbers2", subtractor)
graph.add_node("second_router", lambda state:state)

graph.add_edge(START, "first_router")

graph.add_conditional_edges("first_router", first_router, {
    "add_numbers_edge": "add_numbers",
    "subtract_numbers_edge": "subtract_numbers"
})

graph.add_edge("add_numbers", "second_router")
graph.add_edge("subtract_numbers", "second_router")

graph.add_conditional_edges("second_router", second_router, {
    "add_numbers_edge2": "add_numbers2",
    "subtract_numbers_edge2": "subtract_numbers2"
})

graph.add_edge("add_numbers", END)
graph.add_edge("subtract_numbers", END)

app = graph.compile()

initial_state = AgentState(number1=10, number2=5, operation1='-', number3=7, number4=2, operation2='+')

result = app.invoke(initial_state)

print(result['result'])

image_data = app.get_graph().draw_mermaid_png()
with open("04_graph.png", "wb") as f:
    f.write(image_data)

print("Graph image saved as graph.png")
