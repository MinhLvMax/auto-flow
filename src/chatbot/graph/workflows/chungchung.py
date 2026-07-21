from langgraph.graph import StateGraph, START, END
from src.chatbot.graph.state import State
from src.chatbot.graph.nodes import StorageAnalysisNode

def build_storage_analysis_graph():
    """Luồng phụ xử lý phân tích và thống kê thông số thư mục kho tài nguyên"""
    graph = StateGraph(State)
    graph.add_node(StorageAnalysisNode.__name__, StorageAnalysisNode())
    graph.add_edge(START, StorageAnalysisNode.__name__)
    graph.add_edge(StorageAnalysisNode.__name__, END)
    return graph.compile()