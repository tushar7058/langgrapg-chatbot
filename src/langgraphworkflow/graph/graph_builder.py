import os
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from src.langgraphworkflow.state.state import State
from src.langgraphworkflow.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphworkflow.nodes.chatbot_with_tool_node import ChatbotwithToolNode
from src.langgraphworkflow.nodes.ai_news_node import AINewsNode
from src.langgraphworkflow.nodes.blog_generation_node import BlogGenerationNode
from src.langgraphworkflow.tools.search_tool import get_tools, create_tool_node

class GraphBuilder:
    def __init__(self, model):
        self.llm = model

    def basic_chatbot_build_graph(self):
        """
        Build a basic chatbot graph: START -> chatbot -> END
        """
        builder = StateGraph(State)
        basic_node = BasicChatbotNode(self.llm)
        builder.add_node("chatbot", basic_node.process)
        builder.add_edge(START, "chatbot")
        builder.add_edge("chatbot", END)
        return builder.compile()

    def chatbot_with_tools_build_graph(self):
        """
        Build an advanced chatbot graph with web search tool integration.
        """
        has_tavily = bool(os.getenv("TAVILY_API_KEY") or os.getenv("TAVILY_SEARCH_API_KEY"))
        if has_tavily:
            try:
                tools = get_tools()
                tool_node = create_tool_node(tools)
                obj_chatbot_with_node = ChatbotwithToolNode(self.llm)
                chatbot_node = obj_chatbot_with_node.create_chatbot(tools)

                builder = StateGraph(State)
                builder.add_node("chatbot", chatbot_node)
                builder.add_node("tools", tool_node)

                builder.add_edge(START, "chatbot")
                builder.add_conditional_edges("chatbot", tools_condition)
                builder.add_edge("tools", "chatbot")
                return builder.compile()
            except Exception:
                pass

        # Fallback to basic graph if tools cannot be initialized
        return self.basic_chatbot_build_graph()

    def ai_news_build_graph(self):
        """
        Build an AI News research and generation graph.
        """
        has_tavily = bool(os.getenv("TAVILY_API_KEY") or os.getenv("TAVILY_SEARCH_API_KEY"))
        tools = None
        if has_tavily:
            try:
                tools = get_tools()
            except Exception:
                tools = None

        ai_news_obj = AINewsNode(self.llm)
        news_node = ai_news_obj.create_news_agent(tools=tools)

        builder = StateGraph(State)
        builder.add_node("news_agent", news_node)
        builder.add_edge(START, "news_agent")

        if tools:
            tool_node = create_tool_node(tools)
            builder.add_node("tools", tool_node)
            builder.add_conditional_edges("news_agent", tools_condition)
            builder.add_edge("tools", "news_agent")
        else:
            builder.add_edge("news_agent", END)

        return builder.compile()

    def blog_generation_build_graph(self):
        """
        Build a Blog Generation graph.
        """
        has_tavily = bool(os.getenv("TAVILY_API_KEY") or os.getenv("TAVILY_SEARCH_API_KEY"))
        tools = None
        if has_tavily:
            try:
                tools = get_tools()
            except Exception:
                tools = None

        blog_obj = BlogGenerationNode(self.llm)
        blog_node = blog_obj.create_blog_agent(tools=tools)

        builder = StateGraph(State)
        builder.add_node("blog_agent", blog_node)
        builder.add_edge(START, "blog_agent")

        if tools:
            tool_node = create_tool_node(tools)
            builder.add_node("tools", tool_node)
            builder.add_conditional_edges("blog_agent", tools_condition)
            builder.add_edge("tools", "blog_agent")
        else:
            builder.add_edge("blog_agent", END)

        return builder.compile()

    def setup_graph(self, usecase: str):
        """
        Set up and compile the LangGraph workflow based on the chosen usecase.
        """
        normalized_usecase = usecase.strip().lower()

        if normalized_usecase == "basic chatbot":
            return self.basic_chatbot_build_graph()
        elif normalized_usecase in ["chatbot with tool", "chatbot with web", "chatbot_with_web"]:
            return self.chatbot_with_tools_build_graph()
        elif normalized_usecase in ["ai news", "ai_news"]:
            return self.ai_news_build_graph()
        elif normalized_usecase in ["blog generation", "blog_generation"]:
            return self.blog_generation_build_graph()
        else:
            return self.basic_chatbot_build_graph()
