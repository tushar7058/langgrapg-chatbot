import os
from pathlib import Path
from configparser import ConfigParser

class Config:
    def __init__(self, config_file=None):
        self.config = ConfigParser()
        if config_file is None:
            # Default to uiconfigui.ini in the same directory as this file
            default_path = Path(__file__).parent / "uiconfigui.ini"
            if default_path.exists():
                config_file = str(default_path)
            else:
                config_file = "./src/langgraphworkflow/ui/uiconfigui.ini"
        
        self.config.read(config_file)

    def get_llm_options(self):
        val = self.config.get("DEFAULT", "LLM_OPTIONS", fallback="Groq")
        return [opt.strip() for opt in val.split(",") if opt.strip()]

    def get_usecase_options(self):
        val = self.config.get("DEFAULT", "USECASE_OPTIONS", fallback="Basic Chatbot, Chatbot with Tool, AI News, Blog Generation")
        return [opt.strip() for opt in val.split(",") if opt.strip()]

    def get_groq_model_options(self):
        val = self.config.get("DEFAULT", "GROQ_MODEL_OPTIONS", fallback="llama-3.3-70b-versatile, llama-3.1-8b-instant")
        return [opt.strip() for opt in val.split(",") if opt.strip()]

    def get_page_title(self):
        return self.config.get("DEFAULT", "PAGE_TITLE", fallback="Agentic Chatbot : LangGraph")
