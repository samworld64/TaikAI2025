import streamlit as st
from information import questionnaire
from response import display_response
from weather import display_weather
from streamlit_card import card

app_mode = "Welcome"



def main():
    # Set page config for wide mode
    st.set_page_config(
        page_title="HarvestIQ",
        page_icon="/asset/icon.svg",
        menu_items={
            "About": "HarvestIQ is an AI-powered smart agriculture advisor designed to support farmers worldwide, especially in Africa. By combining local farming knowledge with cutting-edge AI, HarvestIQ delivers accurate weather forecasts, rain predictions, and personalized crop planting recommendations. Our mission is to bridge technology and tradition, helping farmers boost productivity, reduce risks, and make data-driven decisions while honoring cultural farming practices.",
            "Get help": None,
            "Report a Bug": None
        },
        layout="wide"
    )

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("style.css")

    # st.sidebar.title("Navigation")
    # app_mode = st.sidebar.selectbox("Choose the section", ["Welcome", "Fill Questionnaire", "Chat", "Figma"])
    # Sidebar navigation
    with st.sidebar:
        st.image("asset/petal-logo-w.png")
        st.markdown("## Navigation")
        st.button("Home", on_click=lambda: setattr(st.session_state, 'current_page', 'welcome'))
        st.button("Information", on_click=lambda: setattr(st.session_state, 'current_page', 'questions'))
        st.button("Weather", on_click=lambda: setattr(st.session_state, 'current_page', 'weather'))
        st.button("Planting Time", on_click=lambda: setattr(st.session_state, 'current_page', 'planting_time'))
        st.button("Prediction", on_click=lambda: setattr(st.session_state, 'current_page', 'prediction'))
        st.button("Help", on_click=lambda: setattr(st.session_state, 'current_page', 'help'))

        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

    # set openai key
    st.session_state.openai_api_key = openai_api_key


    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'welcome'  # Default page

    if st.session_state['current_page'] == 'welcome':
        welcome_page()
    elif st.session_state['current_page'] == 'questions':
        questionnaire()
    # elif st.session_state['current_page'] == 'chat':
    #     display_response(openai_api_key=openai_api_key)
    elif st.session_state['current_page'] == 'weather':
        display_weather(openai_api_key=openai_api_key, target='weather')
    elif st.session_state['current_page'] == 'planting_time':
        display_weather(openai_api_key=openai_api_key, target='planting_time')
    elif st.session_state['current_page'] == 'prediction':
        display_weather(openai_api_key=openai_api_key, target='prediction')

def welcome_page():

    st.image("asset/harvest_cover.png")

    def create_card(title, text, is_active=False):
        return card(
            title=title,
            text=text,
            image=None,
            # image="http://placekitten.com/300/250",
            styles={ "card": {
                    "width": "100%",
                    "filter": "drop-shadow(0px 23px 12px rgba(0,0,0,0.10000000149011612))",
                    "border-radius":"20px",
                    "margin": "20px",
                    "padding":"20px",
                    "display":"flex",
                    "flex-direction":"column",
            #         "gap":"30px",
                    "border":"1px solid blue" if is_active else "none",
                    "outline": "blue" if is_active else "none"
                    },
                    "text": {
                        "color": "#555"
                    },
                    "title": {
                        "color": "#333",
                        "font-size": "1.4em"
                    },
                    "filter": {
                        "background-color": "#a8eb12",  # <- make the image not dimmed anymore  
                        "background-image": "linear-gradient(120deg, #d4fc79 0%, #96e6a1 100%)"
                    }
            }

        )

    col1, col2, col3 = st.columns(3)

    with col1:
        create_card("Weather Outlook", "HarvestIQ provides farmers with accurate, real-time weather forecasts tailored to their specific locations. This feature analyzes meteorological data to deliver insights on temperature, humidity, wind patterns, and potential weather events, helping farmers make informed decisions about their daily activities.")

    with col2:
        create_card("Best Planting Times", "HarvestIQ analyzes historical weather data to recommend the best planting times for various crops, helping farmers optimize their planting schedules and improve yields.")

    with col3:
        create_card("Rain Prediction", "With advanced algorithms, HarvestIQ offers reliable rain predictions, alerting farmers to upcoming rainfall events. This feature enables proactive planning for irrigation, soil management, and harvesting activities, reducing risks associated with unexpected weather changes and enhancing overall productivity.")
    
        st.button("Get Started", on_click=lambda: setattr(st.session_state, 'current_page', 'questions'))
        

if __name__ == "__main__":
    main()

