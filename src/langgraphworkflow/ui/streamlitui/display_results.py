import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

class DisplayResultStreamlit:
    def __init__(self, usecase: str, graph, user_message: str):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        """
        Execute the compiled LangGraph workflow and render intermediate tool execution and final assistant response.
        """
        # Ensure session state messages list exists
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        # Convert session history into LangChain messages format for graph input
        history = []
        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                history.append(AIMessage(content=msg["content"]))

        # Append current user message
        history.append(HumanMessage(content=self.user_message))

        initial_state = {"messages": history}

        with st.chat_message("assistant"):
            status_placeholder = st.empty()
            response_placeholder = st.empty()
            tool_logs = []

            try:
                # Stream or invoke graph
                final_response_content = ""
                with st.spinner("🤖 Thinking..."):
                    result = self.graph.invoke(initial_state)

                if result and "messages" in result:
                    messages = result["messages"]

                    # Process messages from execution
                    for message in messages:
                        if isinstance(message, ToolMessage):
                            tool_name = getattr(message, "name", "Web Search Tool")
                            content_snippet = str(message.content)[:300] + ("..." if len(str(message.content)) > 300 else "")
                            tool_logs.append(f"**{tool_name}**: {content_snippet}")
                        elif isinstance(message, AIMessage) and message.content:
                            # The latest AIMessage with text content is the answer
                            final_response_content = message.content

                # Show tool activities if any
                if tool_logs:
                    with st.expander("🛠️ Tool Invocations & Research Data", expanded=False):
                        for log in tool_logs:
                            st.markdown(log)

                # Render response
                if final_response_content:
                    response_placeholder.markdown(final_response_content)
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": final_response_content
                    })
                else:
                    fallback = "I processed your request, but did not generate any output."
                    response_placeholder.markdown(fallback)
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": fallback
                    })

            except Exception as e:
                err_msg = f"❌ Error during workflow execution: {str(e)}"
                response_placeholder.error(err_msg)
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": err_msg
                })
