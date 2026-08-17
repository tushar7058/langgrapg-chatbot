import streamlit as st
from src.langgraphworkflow.ui.uiconfig import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖"+self.config.get_page_title(),layout="wide")
        st.header("🤖"+self.config.get_page_title())

        with st.sidebar:
            # to get llm options
            llm_options =self.config.get_llm_option()
            usecase_options= self.config.get_use_case_options()

            # llm selection
            self.user_controls["selected_llm"]= st.selectbox("select LLm",llm_options)

            if self.user_controls["selected_llm"]=="Groq":
                # model selection 
                groq_model_option = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"]= st.selectbox("select model",groq_model_option)
                self.user_controls["groq_api_key"]= st.session_state["groq_api_key"]= st.text_input("API KEY",type="password")
                # validate api key
                if not self.user_controls["groq_api_key"]:
                    st.warning("Please enter your GROQ API Key")

            # use case selection
            self.user_controls["selected_usecase"]=st.selectbox("Select use cases",usecase_options)

        return self.user_controls

 
  

 

