from langchain_core.messages import SystemMessage, HumanMessage
from src.langgraphworkflow.state.state import State

class AINewsNode:
    """
    AI News research and synthesis agent node.
    """
    def __init__(self, model):
        self.llm = model

    def create_news_agent(self, tools=None):
        """
        Create a news agent node with optional search tool binding.
        """
        system_prompt = SystemMessage(
            content=(
                "You are an expert AI Tech Journalist and Technology Analyst. "
                "Your objective is to provide comprehensive, timely, and insightful news reports on Artificial Intelligence, "
                "Machine Learning, LLMs, and tech developments. "
                "When answering, structure your response professionally with:\n"
                "- 🚀 **Executive Summary**\n"
                "- 🔬 **Key Breakthroughs & Announcements**\n"
                "- 🏢 **Industry Impact & Enterprise Use Cases**\n"
                "- 💡 **Expert Analysis & Future Outlook**\n"
                "- 🔗 **Key Takeaways & Citations**\n"
                "If search tools are available, use them to find the most recent information."
            )
        )

        llm_engine = self.llm.bind_tools(tools) if tools else self.llm

        def news_node(state: State) -> dict:
            messages = state["messages"]
            # Ensure system prompt is prepended if not present
            if not messages or not isinstance(messages[0], SystemMessage):
                full_messages = [system_prompt] + list(messages)
            else:
                full_messages = messages

            response = llm_engine.invoke(full_messages)
            return {"messages": [response]}

        return news_node
