import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self , user_control_input):
        self.user_control_input = user_control_input

    def get_llm_model(self):
        try:
            groq_api_key=self.user_control_input["groq_api_key"]
            selected_groq_model=self.user_control_input["selected_groq_model"]
            
            if groq_api_key =='' and os.environ["GROQ_API_KEY"]=='':
                st.error("Please enter your groq api key")
                return None
            
            llm = ChatGroq(
                model=selected_groq_model,
                groq_api_key=groq_api_key,
                temperature=0.5,
                max_tokens=1000
            )
        except Exception as e:
            st.error(f"Error: {e}")
            return None
        

        return llm

            
            

