from src.langgraphworkflow.state.state import  State
class BasicChatbotNode:
    """
    basic chatbot logic implementation
    """
    def __init__(self,model):
        self.llm = model


    def process(self,state:State)->dict:
        """
        process the input state  and generate chatbot reponse.

        """

        return {"messages":self.llm.invoke(state['messages'])}