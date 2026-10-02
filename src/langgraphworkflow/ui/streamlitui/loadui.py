import os
import streamlit as st
from dotenv import load_dotenv
from src.langgraphworkflow.ui.uiconfig import Config

load_dotenv()

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        page_title = self.config.get_page_title()
        st.set_page_config(
            page_title=page_title,
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        with st.sidebar:
            st.title("⚙️ Configuration")
            st.markdown("---")

            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            groq_models = self.config.get_groq_model_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox(
                "🤖 Select LLM Provider",
                options=llm_options,
                index=0
            )

            # Model selection
            if self.user_controls["selected_llm"] == "Groq":
                self.user_controls["selected_groq_model"] = st.selectbox(
                    "🧠 Select Model",
                    options=groq_models,
                    index=0
                )

                # API Key with .env fallback prefill
                default_groq_key = os.getenv("GROQ_API_KEY", "")
                groq_key_input = st.text_input(
                    "🔑 Groq API Key",
                    value=default_groq_key,
                    type="password",
                    help="Get your key at https://console.groq.com/keys"
                )
                self.user_controls["GROQ_API_KEY"] = groq_key_input
                if groq_key_input:
                    os.environ["GROQ_API_KEY"] = groq_key_input
                else:
                    st.warning("⚠️ Enter GROQ API key to proceed.")

            st.markdown("---")
            # Usecase selection
            self.user_controls["selected_usecase"] = st.selectbox(
                "🎯 Select Usecase",
                options=usecase_options,
                index=0
            )

            # Optional Tavily Key for web tools
            requires_tavily = self.user_controls["selected_usecase"] in [
                "Chatbot with Tool",
                "AI News",
                "Blog Generation"
            ]

            if requires_tavily:
                default_tavily_key = os.getenv("TAVILY_API_KEY") or os.getenv("TAVILY_SEARCH_API_KEY", "")
                tavily_key_input = st.text_input(
                    "🌐 Tavily API Key (Web Search)",
                    value=default_tavily_key,
                    type="password",
                    help="Get your key at https://app.tavily.com/home"
                )
                self.user_controls["TAVILY_API_KEY"] = tavily_key_input
                if tavily_key_input:
                    os.environ["TAVILY_API_KEY"] = tavily_key_input
                else:
                    st.info("ℹ️ Tavily API key is optional for search. Without it, standard LLM knowledge is used.")

            st.markdown("---")
            # Clear chat button
            if st.button("🗑️ Clear Conversation", use_container_width=True):
                st.session_state["messages"] = []
                st.session_state["last_usecase"] = self.user_controls["selected_usecase"]
                st.rerun()

            st.caption("Built with LangGraph & Streamlit")

        return self.user_controls