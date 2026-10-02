
from langgraph.graph import StateGraph , START , END

from langgraphworkflow.tools.search_tool import create_tool_node
from src.langgraphworkflow.state.state import State
from src.langgraphworkflow.nodes.basic_chatbot_node import  BasicChatbotNode
from src.langgraphworkflow.tools.search_tool import get_tools
from langgraph.prebuilt import  tools_condition , ToolNode
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

    def chatbot_with_tools_build_graph(self):

        """
        build an advance chatbot graph with tool integration.
        this method creates chatbot graph that includer both a chatbot node
        and a tool . it defines tools, initializes a chatbot with tool
        capabilites , and set up conditional and direct edges between nodes.
        that chatbot node is set as an entry point.
        
        """
        pass
        ## Define a tool and toolnode
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # define llm
        llm = self.llm

        # define a chatbot node


        # add nodes
        self.graph_builder.add_node("chatbot",)
        self.graph_builder.add_node("tools",tool_node)


        # Define conditional and Direct edges
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")


    def setup_graph(self,usecase:str):
        """
        sets up the graph for the selected use case

        """
        if usecase =="Basic Chatbot":
            self.basic_chatbot_build_graph()
            return self.graph_builder.compile()

        if usecase == "chatbot_with_web":
            self.chatbot_with_tools_build_graph()

        return self.graph_builder.compile()




