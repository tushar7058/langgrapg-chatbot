from langchain_community.tools.tavily_search import  TavilySearchResults
from dotenv import load_dotenv
load_dotenv(dotenv_path='/Users/tushark/Developer/langgrapg-chatbot/.env')
from langgraph.prebuilt import ToolNode


def get_tools():
    """
    return all tool available

    """
    tools = [TavilySearchResults(max_results =2)]
    return tools

def create_tool_node(tools):

    """
    create and returns a tool node for graph
    """
    return ToolNode(tools)
