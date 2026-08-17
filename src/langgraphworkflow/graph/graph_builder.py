
from langgraph.graph import StateGraph , START , END
from src.langgraphworkflow.state.state import State
from src.langgraphworkflow.nodes.basic_chatbot_node import  BasicChatbotNode

class GraphBuilder:
    def __init__(self,model):
        self.llm =model
        self.graph_builder = StateGraph(State)


    def basic_chatbot_build_graph(self):
        """
        Builds a chatbot graph using langgraph
        This method intialize a chatbot node using the basichatbotnode class
        and integrats it into the graph. the chatbot node  is set as both the
        entry and exit point of graph.

        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)


    def setup_graph(self,usecase:str):
        """
        sets up the graph for the selected use case

        """
        if usecase =="Basic Chatbot":
            self.basic_chatbot_build_graph()
            return self.graph_builder.compile()



