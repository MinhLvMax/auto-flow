from langgraph.graph import StateGraph, START, END
from src.chatbot.graph.state import State
from src.chatbot.graph.nodes import ClassificationNode, ExtractEntitiesNode, NaturalChatNode, SearchNode, \
    RetrievalChatNode
from src.chatbot.graph.router import classification_router
from src.chatbot.graph.workflows.natural_chat import build_natural_graph

def build_workflow():
    graph = StateGraph(State)

    graph.add_node(ClassificationNode.__name__, ClassificationNode())
    graph.add_conditional_edges(
        ClassificationNode.__name__,
        classification_router,
    )
    graph.add_node(ExtractEntitiesNode.__name__, ExtractEntitiesNode())
    graph.add_node(build_natural_graph.__name__, build_natural_graph())
    # graph.add_node(NaturalChatNode.__name__, NaturalChatNode())
    graph.add_node(SearchNode.__name__, SearchNode())
    graph.add_node(RetrievalChatNode.__name__, RetrievalChatNode())

    graph.set_entry_point(ClassificationNode.__name__)

    graph.add_edge(ExtractEntitiesNode.__name__, SearchNode.__name__)
    graph.add_edge(SearchNode.__name__, RetrievalChatNode.__name__)

    return graph.compile()

if __name__ == '__main__':
    graph = build_workflow()
    from src.chatbot.models.history import History
    from pprint import pprint
    history = History()
    while True:
        user_input = input('Enter a sentence: ')
        if user_input == '':
            break
        history.add('user', user_input)
        state = State(history=history)
        last_row_state = graph.invoke(state)
        last_state = State.model_validate(last_row_state)
        system_output = last_state.history.last().get('content')
        history.add('assistant', system_output)
        print(system_output)
        pprint(last_state.found_paths)
