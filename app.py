import streamlit as st
from information import questionnaire, compile_user_data
from response import display_response
from weather import display_weather
from streamlit_card import card
from alert import display_alert
from planting import display_planting
from prediction import display_prediction
from help import display_help

app_mode = "Welcome"



def main():
    # Set page config for wide mode
    st.set_page_config(
        page_title="HarvestIQ",
        page_icon="asset/harvestiq-logo.svg",
        menu_items={
            "About": "HarvestIQ is an AI-powered smart agriculture advisor designed to support farmers in the entire world specially in africa. By combining local farming knowledge with cutting-edge AI, HarvestIQ delivers accurate weather forecasts, rain predictions, and personalized crop planting recommendations. Our mission is to bridge technology and tradition, helping farmers boost productivity, reduce risks, and make data-driven decisions while honoring cultural farming practices.",
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
        st.button("Planting Time", on_click=lambda: setattr(st.session_state, 'current_page', 'planting'))
        st.button("Rain Prediction", on_click=lambda: setattr(st.session_state, 'current_page', 'prediction'))
        st.button("Peste Alert", on_click=lambda: setattr(st.session_state, 'current_page', 'alert'))
        st.button("Help", on_click=lambda: setattr(st.session_state, 'current_page', 'help'))
        # st.button("Figma Welcome", on_click=lambda: setattr(st.session_state, 'current_page', 'figma_welcome'))
        # st.button("Figma Profile", on_click=lambda: setattr(st.session_state, 'current_page', 'figma_profile'))
        # st.button("Clinics", on_click=lambda: setattr(st.session_state, 'current_page', 'clinics'))

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
    elif st.session_state['current_page'] == 'chat':
        display_response(openai_api_key=openai_api_key)
   
    elif st.session_state['current_page'] == 'weather':
         user_data = compile_user_data()  # This gets all the info from the questionnaire
         display_weather(user_data=user_data, openai_api_key=st.session_state.openai_api_key)
    
    elif st.session_state['current_page'] == 'alert':
        user_data = compile_user_data()
        display_alert(openai_api_key=openai_api_key)
    elif st.session_state['current_page'] == 'help':
            user_data = compile_user_data()  # This gets all the info from the questionnaire
            display_help(user_data=user_data, openai_api_key=st.session_state.openai_api_key)

    elif st.session_state['current_page'] == 'planting':
        user_data = compile_user_data()
        display_planting(openai_api_key=openai_api_key)
    elif st.session_state['current_page'] == 'prediction':
        user_data = compile_user_data()
        display_prediction(openai_api_key=openai_api_key)
    # elif st.session_state['current_page'] == 'figma_welcome':
    #     figma_welcome()
    # elif st.session_state['current_page'] == 'figma_profile':
    #     figma_profile()
    # elif st.session_state['current_page'] == 'clinics':
    #     clinics()
        
def figma_welcome():
    st.title("Figma Welcome Page")
    st.write("Welcome to the Figma section! Here you can find various resources and tools related to Figma.")

def figma_profile():
    st.title("Figma Profile Page")
    st.write("This is your Figma profile. You can manage your designs and projects here.")

def clinics():
    st.title("Clinics Page")
    st.write("Welcome to the Clinics section! Here you can find information about various clinics.")

def welcome_page():
    st.title("Welcome to HarvestIQ")

    #st.image("asset/harvest_cover.png")
    st.image("asset/homebg.png")

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
                    "margin": "0.1px",
                    "padding":"0.1px",
                    "display":"flex",
                    "flex-direction":"column",
            #         "gap":"30px",
                    "border":"1px solid blue" if is_active else "none",
                    "outline": "blue" if is_active else "none"
                    },
                    "text": {
                        "color": "#555",
                        "font-size": "0.7em"  # Change to "0.95em" or "14px" if needed
                    },
                    "title": {
                        "color": "#333",
                        "font-size": "1.4em"
                    },
                    "filter": {
                        "background-color": "#1b0ceb",  # <- make the image not dimmed anymore  
                        "background-image": "linear-gradient(120deg, #d4fc79 0%, #96e6a1 100%)"
                    }
            }

        )

    col1, col2, col3 = st.columns(3)

    with col1:
        create_card("Weather Outlook", "HarvestIQ provides farmers with accurate, real-time weather forecasts tailored to their specific locations. This feature analyzes meteorological data to deliver insights on temperature, humidity, wind patterns, and potential weather events, helping farmers make informed decisions about their daily activities.")

    with col2:
        create_card("Best Planting Times & Pest Alert", "HarvestIQ analyzes historical weather data to recommend the best planting times for various crops, helping farmers optimize their planting schedules and improve yields. Additionally, the pest alert feature notifies farmers of potential pest outbreaks in their area, allowing for timely interventions to protect crops and minimize damage.", is_active=True)

    with col3:
        create_card("Rain Prediction", "With advanced algorithms, HarvestIQ offers reliable rain predictions, alerting farmers to upcoming rainfall events. This feature enables proactive planning for irrigation, soil management, and harvesting activities, reducing risks associated with unexpected weather changes and enhancing overall productivity.")
    
        st.button("Get Started", on_click=lambda: setattr(st.session_state, 'current_page', 'questions'))
        

if __name__ == "__main__":
    main()

