from langchain_core.messages import SystemMessage
from src.langgraphworkflow.state.state import State

class BlogGenerationNode:
    """
    Blog generation agent node for creating detailed, high-quality, structured articles.
    """
    def __init__(self, model):
        self.llm = model

    def create_blog_agent(self, tools=None):
        """
        Create a blog writer agent node.
        """
        system_prompt = SystemMessage(
            content=(
                "You are an award-winning Content Strategist and Technical Blog Writer. "
                "Your mission is to produce in-depth, engaging, SEO-optimized, and well-structured blog posts "
                "based on the user's requested topic.\n\n"
                "Follow this comprehensive format for every blog post:\n"
                "1. **Catchy Title** (H1)\n"
                "2. **Engaging Introduction** (Hook the reader, explain why this topic matters now)\n"
                "3. **Table of Contents / Overview**\n"
                "4. **Detailed Core Sections** (H2 and H3 with deep insights, real-world examples, or code/diagrams if relevant)\n"
                "5. **Best Practices / Tips for Success**\n"
                "6. **Key Takeaways & Summary**\n"
                "7. **Call to Action (CTA)**\n"
                "8. **Suggested SEO Meta Description & Tags**\n\n"
                "Maintain a professional, conversational, and highly informative tone."
            )
        )

        llm_engine = self.llm.bind_tools(tools) if tools else self.llm

        def blog_node(state: State) -> dict:
            messages = state["messages"]
            if not messages or not isinstance(messages[0], SystemMessage):
                full_messages = [system_prompt] + list(messages)
            else:
                full_messages = messages

            response = llm_engine.invoke(full_messages)
            return {"messages": [response]}

        return blog_node
