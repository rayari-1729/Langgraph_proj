# multi node

from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: int
    skills: list[str]
    result: str

def greet_first_node(state: AgentState) -> AgentState:
    """Greet the user with their name"""
    state['result'] = f"Hey {state['name']}, welcome to the world of agents!"
    return state

def describe_age_second_node(state: AgentState) -> AgentState:
    """Describe the age of the user"""
    state['result'] = state['result'] + f" You are {state['age']} years old."
    return state

def describe_skills_third_node(state: AgentState) -> AgentState:
    """Describe the skills of the user"""
    state['result'] = state['result'] + f" You have skills in: {state['skills']}."
    return state

graph = StateGraph(AgentState)

graph.add_node("greet_first_node", greet_first_node)
graph.add_node("describe_age_second_node", describe_age_second_node)
graph.add_node("describe_skills_third_node", describe_skills_third_node)

graph.set_entry_point("greet_first_node")
graph.add_edge("greet_first_node", "describe_age_second_node")
graph.add_edge("describe_age_second_node", "describe_skills_third_node")
graph.set_finish_point("describe_skills_third_node")

app = graph.compile()

result = app.invoke({"name": "John", "age": 25, "skills": ["Python", "JavaScript", "SQL"]})

print(result["result"])