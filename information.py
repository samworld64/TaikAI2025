import streamlit as st
from st_audiorec import st_audiorec
from assistant import HarvestIQAssistant
import datetime

def collect_personal_info():
    # Personal Information
    st.number_input("What is your age?", min_value=18, max_value=80, key="age")
    st.selectbox("What is your gender identity?", ["Male", "Female", "Prefer not to say"], key="gender")
    
    navigate()

def collect_address_location():
    # Address and Location
    st.text_input("What is your current address?", key="address")
    st.text_input("What is your city name?", key="city")
    st.text_input("What is your country name?", key="country")
    st.text_input("What is your latitude?", key="latitude")
    st.text_input("What is your longitude?", key="longitude")

    navigate()


def privacy_consent():
    # Feedback and Consent
    st.radio("Do you consent to have this information used to tailor health advice specifically for you?", ["No", "Yes"], key="consent")

    def prev():
        if st.session_state.page_number > 0:
            st.session_state.page_number -= 1
    def finish():
        user_data = compile_user_data()
        st.session_state['information_updated'] = True
        st.success("Profile Submitted Successfully!")
        # st.info(user_data)
        st.session_state['current_page'] = 'chat'

    col1, col2 = st.columns(2)

    col1.button("Back", on_click=prev)
    if st.session_state.consent == "Yes":
        col2.button("Finish", on_click=finish)

    

questionnaire_pages = [
        ("Personal Information", collect_personal_info),
        ("Address Location", collect_address_location),
        ("Privacy", privacy_consent)
]

def questionnaire():

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0

    if st.session_state.page_number < len(questionnaire_pages):
        page_title, page_function = questionnaire_pages[st.session_state.page_number]
        st.progress((st.session_state.page_number + 1) / len(questionnaire_pages))
        st.header(page_title)
        page_function()
        # Store all current input widgets in session_state as 'information_data'
        if 'information_data' not in st.session_state:
            st.session_state['information_data'] = {}
        # Only store relevant keys (filter out Streamlit system keys)
        for key in st.session_state.keys():
            if not key.startswith('_') and key not in ['page_number', 'current_page', 'information_updated', 'information_data']:
                value = st.session_state[key]
                # Ensure address is always a string, never None
                if key == 'address':
                    st.session_state['information_data'][key] = value if value is not None else ""
                else:
                    st.session_state['information_data'][key] = value
    else:
        st.session_state.page_number = 0  # Reset for reusability

def navigate():
    def prev():
        if st.session_state.page_number > 0:
            st.session_state.page_number -= 1
    def next():
        if st.session_state.page_number < len(questionnaire_pages) - 1:
            st.session_state.page_number += 1

    col1, col2 = st.columns(2)

    col1.button("Back", on_click=prev)
    col2.button("Next", on_click=next)

def compile_user_data():
    # Gather user data from Streamlit's session state
    # Prefer returning the latest questionnaire data from session_state
    
    # Prefer returning the latest questionnaire data from session_state
    if 'information_data' in st.session_state:
        return st.session_state['information_data']
    else:
        address = st.session_state.get('address', '').strip()
        city = st.session_state.get('city', '').strip()
        country = st.session_state.get('country', '').strip()
        location_parts = [part for part in [address, city, country] if part]
        location = ', '.join(location_parts) if location_parts else ''

        user_data = {
            'age': st.session_state.get('age', 'Not specified'),
            'gender': st.session_state.get('gender', 'Not specified'),
            'location': location,
            'latitude': st.session_state.get('latitude', 'Not specified'),
            'longitude': st.session_state.get('longitude', 'Not specified'),
            'consent': st.session_state.get('consent', 'No'),
            'target': 'weather'
        }
        return user_data
