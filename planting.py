import streamlit as st
from io import BytesIO
from assistant import HarvestIQAssistant
from information import compile_user_data


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


def display_planting(user_data=None, openai_api_key=None):
    st.title("Best Planting Time")
    if user_data is None:
        user_data = compile_user_data()
    ## this will be changed based on the page we are
    user_data['target'] = 'planting'
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if 'information_updated' not in st.session_state: 
        st.info("Please update your information first to continue.")
        st.stop()
    st.caption("🚀 HarvestIQ Chatbot powered by OpenAI LLM")
    assistant = HarvestIQAssistant(openai_api_key)
    response = assistant.generate_response(user_data, openai_api_key)
    ## convert to speech
    assistant.text_to_speech(response, "nova")
    autoplay_audio("audio.mp3")
    st.chat_message("assistant").write(response)
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I further assist you?"}]
    st.chat_message("assistant").write("How can I further assist you?")
    # for msg in st.session_state.messages:
    #     st.chat_message(msg["role"]).write(msg["content"])
    # if prompt := st.chat_input("You: "):
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #     st.chat_message("user").write(prompt)
    #     with st.chat_message("assistant"):
    #         response = assistant.generate_response(user_data, openai_api_key)
    #         st.session_state.messages.append({"role": "assistant", "content": response})
    #         st.write(response)
    #         ## convert to speech
    #         assistant.text_to_speech(response, "nova")
    #         autoplay_audio("audio.mp3")   
    #         st.write(response)
    #         st.chat_message("assistant").write(response)
    #         st.session_state.messages.append({"role": "assistant", "content": "How can I further assist you?"})
    #     st.chat_message("assistant").write("How can I further assist you?")
    if prompt := st.chat_input():
        # client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = assistant.chat(messages=st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
        st.session_state.messages.append({"role": "assistant", "content": "How can I further assist you?"})
        st.chat_message("assistant").write("How can I further assist you?")
