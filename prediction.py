import streamlit as st
from io import BytesIO
import base64
from assistant import HarvestIQAssistant
from information import compile_user_data

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def display_prediction(user_data=None, openai_api_key=None):
    st.title("Rain Prediction")
    if user_data is None:
        user_data = compile_user_data()
    user_data['target'] = 'prediction'
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if 'information_updated' not in st.session_state: 
        st.info("Please update your information first to continue.")
        st.stop()
    st.caption("🚀 HarvestIQ Chatbot powered by OpenAI LLM")
    assistant = HarvestIQAssistant(openai_api_key)
    response = assistant.generate_response(user_data, openai_api_key)
    assistant.text_to_speech(response, "nova")
    autoplay_audio("audio.mp3")
    st.chat_message("assistant").write(response)
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I further assist you?"}]
    st.chat_message("assistant").write("How can I further assist you?")
