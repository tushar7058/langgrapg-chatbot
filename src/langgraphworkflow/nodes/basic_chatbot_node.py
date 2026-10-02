from src.langgraphworkflow.state.state import State

class BasicChatbotNode:
    """
    Basic chatbot logic node.
    """
    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Process the input state messages and generate chatbot response.
        """
        response = self.llm.invoke(state["messages"])
        return {"messages": [response]}