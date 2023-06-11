import os

import config
import streamlit as st
from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI


def set_page_config():
    # Set Streamlit page configuration
    st.set_page_config(page_title="What's in that food?", layout="wide")
    st.markdown(
        """
<style>
    [data-testid=stSidebar] {
        background-color: #F2FAFF;
    }
</style>
""",
        unsafe_allow_html=True,
    )


def set_sessions():
    """
    Set Streamlit session states.
    """

    # Initialize session states
    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []
    if "input" not in st.session_state:
        st.session_state["input"] = ""
    if "history" not in st.session_state:
        st.session_state["history"] = []


def get_input():
    """
    Get user input.
    """
    st.text_input(
        "Human",
        st.session_state["input"],
        key="input",
        placeholder="Food assistant here, ask me your questions about the food contents!",
        label_visibility="hidden",
    )


@st.cache_resource
def LLM_chain(
    api_key: str, model_name: str, k: int, temperature: float = 0.0
) -> LLMChain:
    """
    Create a LLMChain object.

    Args:
        api_key (str):
        model_name (str):
        k (int):
        temperature (float, optional): Defaults to 0.0.

    Returns:
        LLMChain:
    """
    davinci = OpenAI(
        openai_api_key=api_key, model_name=model_name, temperature=temperature
    )

    llm_chain = LLMChain(
        llm=davinci,
        memory=ConversationBufferWindowMemory(k=k),
        prompt=config.CUSTOM_MEMORY_CONVERSATION_TEMPLATE,
        verbose=False,
    )

    return llm_chain


def add_sidebar():
    with st.sidebar.expander("🛠️ Options", expanded=False):
        # Option to preview memory buffer
        MODEL = st.selectbox(label="Model", options=config.MODEL_OPTIONS)
        K = st.number_input(
            "(#)Summary of prompts to consider", min_value=6, max_value=12
        )
        st.text("Preview memory buffer")
        st.session_state.history

    return MODEL, K
        
if __name__ == "__main__":
    set_page_config()
    st.title(":rabbit: Wondering more about what's in your food? Try me!")
    st.text(config.warning_message)
    API_KEY = (
        st.secrets["openai_key"]
        if os.path.exists("../.streamlit/secrets.toml") and st.secrets["openai_key"]
        else st.sidebar.text_input("API-KEY", type="password")
    )

    if API_KEY:
        set_sessions()
        model, k = add_sidebar()
        llm_chain = LLM_chain(api_key=API_KEY, model_name=model, k=k)
        get_input()

        if st.session_state.input:
            output = llm_chain.run(input=st.session_state.input)
            st.session_state.past.append(st.session_state.input)
            st.session_state.generated.append(output)
            st.session_state.history = llm_chain.memory.buffer
    else:
        st.error("Please add your OpenAI API key as a secret in the sidebar")
        st.stop()
    
    download_str = []
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        st.info(st.session_state["past"][i], icon="😎")
        st.success(st.session_state["generated"][i], icon="🐰")

        download_str.append(st.session_state["past"][i])
        download_str.append(st.session_state["generated"][i])

    download_str = "\n".join(download_str)
    if download_str:
        st.download_button("Download", download_str)
