from langgraph.graph import StateGraph, START, END
from src.chatbot.graph.state import State
from src.chatbot.graph.nodes import ExtractEntitiesNode, SearchNode, RetrievalChatNode


def build_retrieval_graph():
    """Luồng phụ chuyên xử lý trích xuất thực thể, truy vấn file và phản hồi kết quả tìm kiếm"""
    graph = StateGraph(State)

    # Khai báo các Node nội bộ
    graph.add_node(ExtractEntitiesNode.__name__, ExtractEntitiesNode())
    graph.add_node(SearchNode.__name__, SearchNode())
    graph.add_node(RetrievalChatNode.__name__, RetrievalChatNode())

    # Định nghĩa luồng di chuyển tuyến tính
    graph.add_edge(START, ExtractEntitiesNode.__name__)
    graph.add_edge(ExtractEntitiesNode.__name__, SearchNode.__name__)
    graph.add_edge(SearchNode.__name__, RetrievalChatNode.__name__)
    graph.add_edge(RetrievalChatNode.__name__, END)

    return graph.compile()