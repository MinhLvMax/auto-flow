from src.chatbot.graph.workflow import build_workflow
from src.chatbot.graph.state import State


class ChatbotService:
    def __init__(self, workflow = None):
        self.workflow = workflow or build_workflow()

    def chat(self, message = None):

        result = self.workflow.invoke({
            "query": message
        })

        return result["response"]