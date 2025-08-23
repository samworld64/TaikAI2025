import streamlit as st
from io import BytesIO
from assistant import HarvestIQAssistant

import base64

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


# from assistant import generate_response
from information import compile_user_data

def display_weather(user_data=None, openai_api_key=None):


    if user_data is None:
        user_data = compile_user_data()
    ## this will be changed based on the page we are
    user_data['target'] = 'weather'
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if 'information_updated' not in st.session_state:
        st.info("Please update your information first to continue.")
        st.stop()

    st.title("💬 Weather outlook on your area")
    st.caption("🚀 HarvestIQ Chatbot powered by OpenAI LLM")
    assistant = HarvestIQAssistant(openai_api_key)
    response = assistant.generate_response(user_data, openai_api_key)

    ## convert to speech
    assistant.text_to_speech(response, "nova")
    # audio_file = open("audio.mp3", 'rb')
    # audio_bytes = audio_file.read()
    # st.audio(audio_bytes, format='audio/mpeg')
    autoplay_audio("audio.mp3")

    # st.write(response)
    st.chat_message("assistant").write(response)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I further assist you?"}]

    st.chat_message("assistant").write("How can I further assist you?")

    # for msg in st.session_state.messages:
    #     st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        # client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = assistant.chat(messages=st.session_state.messages)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
