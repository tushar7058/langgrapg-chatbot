import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class GroqLLM:
    def __init__(self, user_control_input: dict):
        self.user_control_input = user_control_input or {}

    def get_llm_model(self):
        try:
            # Check user input first, then fallback to environment variables
            groq_api_key = (
                self.user_control_input.get("GROQ_API_KEY")
                or self.user_control_input.get("groq_api_key")
                or os.getenv("GROQ_API_KEY")
                or ""
            ).strip()

            selected_groq_model = (
                self.user_control_input.get("selected_groq_model")
                or "llama-3.3-70b-versatile"
            ).strip()

            if not groq_api_key:
                st.error("⚠️ GROQ API Key is missing. Please enter your API key in the sidebar or set GROQ_API_KEY in your .env file.")
                return None

            llm = ChatGroq(
                model=selected_groq_model,
                groq_api_key=groq_api_key,
                temperature=0.6,
                max_tokens=2048,
            )
            return llm
        except Exception as e:
            st.error(f"Error initializing Groq LLM: {str(e)}")
            return None
