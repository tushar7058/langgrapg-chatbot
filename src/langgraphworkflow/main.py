import streamlit as st
from src.langgraphworkflow.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphworkflow.llms.groqllm import GroqLLM
from src.langgraphworkflow.graph.graph_builder import GraphBuilder
from src.langgraphworkflow.ui.streamlitui.display_results import DisplayResultStreamlit
def load_langgraph_agentic_app():
    """
    load and run the agentic ai  applicaiton with stramlit ui.
    this fucniton initialize the ui , handle  user input , configures the llm  model ,
    sets up the graph based on selected use case , and display the output while
    implementing exception hadnling for robustness
    """

    # load ui
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    if not user_input:
        st.error("Error:Failed to load user input from the UI")
        return

    user_message = st.chat_input("Enter Your Message")

    if user_message:
        try:
            # config LLM
            obj_llm_config = GroqLLM(user_control_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error:LLM model could not be initialized")
                return
            
            # initialize and setup the graph based on use case
            usecase = user_input.get("selected_usecase")
            if not usecase:
                st.error("Error:no use case selected")
                return

            # graph builder
            graph_builder =GraphBuilder(model=model)
            try:
                graph = graph_builder.setup_graph(usecase=usecase)
                DisplayResultStreamlit(usecase, graph , user_message=user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error:graph setup is failed {e}")
                return

        except Exception as e:
            st.error(f"Error:Graph setup is failed {e}")
            return