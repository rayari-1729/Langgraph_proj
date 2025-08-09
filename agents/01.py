# Personalized compliment agent

from typing import TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    message: str


def personalized_compliment(state: AgentState) -> AgentState:
    """Sends a personalized compliment based on the state."""
    state['message'] = "Hey " + state["message"] + \
        "! You are doing a fantastic job! Keep up the great work!"
    return state


graph = StateGraph(AgentState)

graph.add_node("personalized_compliment", personalized_compliment)

graph.set_entry_point("personalized_compliment")
graph.set_finish_point("personalized_compliment")

app = graph.compile()

result = app.invoke({"message": "John"})

print(result)
