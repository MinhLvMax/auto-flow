from langgraph.graph import StateGraph
from src.chatbot.graph.state import State
from src.chatbot.graph.router import agent_router
from src.chatbot.graph.nodes.agent_node import AgentNode
from src.chatbot.graph.nodes.tool_executor import ToolExecutorNode

def build_agent_graph():
    graph = StateGraph(State)

    graph.add_node(AgentNode.__name__, AgentNode())
    graph.add_node(ToolExecutorNode.__name__, ToolExecutorNode())

    graph.set_entry_point(AgentNode.__name__)

    graph.add_conditional_edges(
        AgentNode.__name__,
        agent_router,
    )

    graph.add_edge(
        ToolExecutorNode.__name__,
        AgentNode.__name__,
    )

    return graph.compile()

if __name__ == '__main__':
    graph = build_agent_graph()
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
        print(system_output)
        pprint(last_state.found_paths)