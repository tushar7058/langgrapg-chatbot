import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools(tavily_api_key: str = None):
    """
    Return all available tools for agents.
    """
    api_key = tavily_api_key or os.getenv("TAVILY_API_KEY") or os.getenv("TAVILY_SEARCH_API_KEY")
    if api_key:
        os.environ["TAVILY_API_KEY"] = api_key
        return [TavilySearchResults(max_results=3, tavily_api_key=api_key)]
    return [TavilySearchResults(max_results=3)]

def create_tool_node(tools):
    """
    Create and return a ToolNode for LangGraph.
    """
    return ToolNode(tools)
