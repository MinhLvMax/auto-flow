from langgraph.graph import StateGraph, START, END
from src.chatbot.graph.nodes import NaturalChatNode
from src.chatbot.graph.state import State

def build_natural_graph():
    graph = StateGraph(State)
    graph.add_node(NaturalChatNode.__name__, NaturalChatNode())
    graph.add_edge(START, NaturalChatNode.__name__)
    graph.add_edge(NaturalChatNode.__name__, END)
    return graph.compile()