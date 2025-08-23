import streamlit as st

def display_help(user_data=None, openai_api_key=None):
    st.title("Help & Frequently Asked Questions")
    st.markdown("""
    Welcome to the **HarvestIQ Help Center**!  
    Here you can find answers to common questions and guidance on how to use the app.
    """)

    with st.expander("🌱 What is HarvestIQ?"):
        st.write("""
        HarvestIQ is an AI-powered smart agriculture advisor designed to support farmers with weather forecasts, rain predictions, and personalized crop recommendations.
        """)

    with st.expander("📝 How do I fill out the questionnaire?"):
        st.write("""
        Go to the 'Fill Questionnaire' page from the sidebar and provide your personal and location information. This helps the AI give you tailored advice.
        """)

    with st.expander("🌦️ How do I get weather information?"):
        st.write("""
        After filling out your location, navigate to the 'Weather' page. The app will use your provided data to show a detailed weather outlook.
        """)

    with st.expander("🌾 How do I get planting recommendations?"):
        st.write("""
        Visit the 'Planting Time' page after completing the questionnaire. The AI will suggest the best planting times and crops for your area.
        """)

    with st.expander("❓ Still need help?"):
        st.write("If you have more questions, please contact the support team or use the chat feature for assistance.")

    # Optional: Add navigation buttons to other pages
    st.markdown("---")
    st.write("**Quick Navigation:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Go to Questionnaire"):
            st.session_state['current_page'] = 'questions'
    with col2:
        if st.button("Go to Weather"):
            st.session_state['current_page'] = 'weather'
    with col3:
        if st.button("Go to Planting Time"):
            st.session_state['current_page'] = 'planting_time'