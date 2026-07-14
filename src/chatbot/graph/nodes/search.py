from src.chatbot.graph.nodes.base_node import BaseNode

class SearchNode(BaseNode):
    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        ...