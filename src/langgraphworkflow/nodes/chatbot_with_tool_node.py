from src.langgraphworkflow.state.state import State

class ChatbotwithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """
    def __init__(self, model):
        self.llm = model

    def create_chatbot(self, tools):
        """
        Return a chatbot node function with tools bound.
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State) -> dict:
            """
            Process the input state messages and generate response with tool calling capability.
            """
            response = llm_with_tools.invoke(state["messages"])
            return {"messages": [response]}

        return chatbot_node