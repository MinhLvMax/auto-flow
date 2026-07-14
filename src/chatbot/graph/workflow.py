from langgraph.graph import StateGraph, START, END
from src.chatbot.graph.state import State
from src.chatbot.graph.nodes import ClassificationNode, ExtractEntitiesNode, NaturalChatNode, SearchNode
from src.chatbot.graph.router import classification_router


def build_workflow():
    graph = StateGraph(State)

    graph.add_node(ClassificationNode.__name__, ClassificationNode)
    graph.add_conditional_edges(
        ClassificationNode.__name__,
        classification_router(ClassificationNode.__name__),
    )
    graph.add_node(ExtractEntitiesNode.__name__, ExtractEntitiesNode)
    graph.add_node(NaturalChatNode.__name__, NaturalChatNode)
    graph.add_node(SearchNode.__name__, SearchNode)

    graph.set_entry_point(ClassificationNode.__name__)

    graph.add_edge(ExtractEntitiesNode.__name__, SearchNode.__name__)

    return graph.compile()

if __name__ == '__main__':
    graph = build_workflow()
