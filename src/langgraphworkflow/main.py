import streamlit as st
from src.langgraphworkflow.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphworkflow.llms.groqllm import GroqLLM
from src.langgraphworkflow.graph.graph_builder import GraphBuilder
from src.langgraphworkflow.ui.streamlitui.display_results import DisplayResultStreamlit

def load_langgraph_agentic_app():
    """
    Load and run the Agentic AI application with Streamlit UI and LangGraph workflows.
    """
    # Initialize UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user controls from the UI.")
        return

    # Header and Usecase banner
    selected_usecase = user_input.get("selected_usecase", "Basic Chatbot")
    selected_model = user_input.get("selected_groq_model", "Llama 3.3")

    # Informative header banner
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%); padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid #374151;">
            <h2 style="color: #f3f4f6; margin: 0; font-size: 1.6rem;">🤖 LangGraph Agentic Assistant</h2>
            <div style="margin-top: 0.5rem; display: flex; gap: 10px; flex-wrap: wrap;">
                <span style="background: #3b82f6; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">🎯 Mode: {selected_usecase}</span>
                <span style="background: #10b981; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">⚡ Model: {selected_model}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Reset chat history if usecase changed
    if "current_usecase" not in st.session_state:
        st.session_state["current_usecase"] = selected_usecase
    elif st.session_state["current_usecase"] != selected_usecase:
        st.session_state["current_usecase"] = selected_usecase
        st.session_state["messages"] = []

    # Display welcome message if history is empty
    if not st.session_state["messages"]:
        welcome_prompts = {
            "Basic Chatbot": "👋 Hello! I am your AI assistant. How can I help you today?",
            "Chatbot with Tool": "👋 Hello! I can assist you and search the live web for the latest facts and answers.",
            "AI News": "🚀 Ready to explore the latest AI breakthroughs, research papers, and industry updates. What AI topic would you like to explore?",
            "Blog Generation": "✍️ Ready to draft a comprehensive, SEO-optimized blog article. What topic or keyword would you like to write about?"
        }
        st.info(welcome_prompts.get(selected_usecase, "👋 How can I help you today?"))

    # Render previous conversation
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input placeholder based on usecase
    input_placeholders = {
        "Basic Chatbot": "Type your message here...",
        "Chatbot with Tool": "Ask a question or request live web research...",
        "AI News": "Enter an AI topic or ask 'What are the top AI news this week?'...",
        "Blog Generation": "Enter a topic (e.g., 'Agentic AI Workflows in 2026') to generate a full blog post..."
    }
    placeholder_text = input_placeholders.get(selected_usecase, "Enter your message...")

    user_message = st.chat_input(placeholder_text)

    if user_message:
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_message)
        st.session_state["messages"].append({"role": "user", "content": user_message})

        try:
            # Configure LLM
            llm_config = GroqLLM(user_control_input=user_input)
            model = llm_config.get_llm_model()

            if not model:
                return

            # Build and execute LangGraph workflow
            graph_builder = GraphBuilder(model=model)
            graph = graph_builder.setup_graph(usecase=selected_usecase)

            DisplayResultStreamlit(
                usecase=selected_usecase,
                graph=graph,
                user_message=user_message
            ).display_result_on_ui()

        except Exception as e:
            st.error(f"❌ Application Error: {str(e)}")