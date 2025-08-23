from openai import OpenAI
from pathlib import Path


class HarvestIQAssistant:

    def __init__(self, api_key) -> None:
        self.api_key = api_key

        self.client = self.get_client()
        # self.assistant, self.thread = self.create_assistant()

    def create_openai_assistant_prompt(self, user_data):

        # Constructing a detailed prompt based on the comprehensive user data collected
        prompt = f"""
            User Profile:
            - Age: {user_data.get('age', '')}
            - Gender: {user_data.get('gender', '')}
            - Location: {user_data.get('location', '')}
            - Latitude: {user_data.get('latitude', '')}
            - Longitude: {user_data.get('longitude', '')}

            User Needs:
        """

        if user_data.get('target') == 'weather':
            prompt = f"Get the weather forecast for location: {user_data.get('location', '')} or latitude: {user_data.get('latitude', '')}, longitude: {user_data.get('longitude', '')}. Provide for the whole week. "
            prompt += '''\nDetails to provide:\n- location\n- temperature\n- condition\n- humidity\n- wind_speed\n- forecast\n'''
            prompt += "\nTask: Provide a detailed weather outlook for the user's area, including a weekly forecast and actionable insights for farmers."
            prompt += "\nRestrict your sources to reliable weather and agricultural resources such as https://www.weather.com/, https://www.noaa.gov/, https://www.agriculture.com/"

        elif user_data.get('target') == 'planting':
            prompt = f"Get the best planting time for location: {user_data.get('location', '')} or latitude: {user_data.get('latitude', '')}, longitude: {user_data.get('longitude', '')}. Provide for the whole year, starting from now. "
            prompt += '''\nDetails to provide:\n- location\n- crops recommended\n- time recommended\n- weather forecast\n'''
            prompt += "\nTask: Recommend optimal planting times and crops for the user's area, based on local climate and agricultural best practices."
            prompt += "\nRestrict your sources to reliable agricultural resources such as https://www.agronomy.org/, https://www.cimmyt.org/, https://www.fao.org/"
        elif user_data.get('target') == 'prediction':
            prompt = f"Get the rain prediction for today for location: {user_data.get('location', '')} or latitude: {user_data.get('latitude', '')}, longitude: {user_data.get('longitude', '')}. "
            prompt += '''\nDetails to provide:\n- location\n- chance_of_rain_today\n- amount_today\n- forecast_today\n- best_time_to_plant_today\n- best_time_to_avoid_today\n'''
            prompt += "\nTask: Provide today's rain prediction and actionable advice for planting and farming activities."
            prompt += "\nRestrict your sources to reliable meteorological and farming resources such as https://www.weather.gov/, https://www.climate.gov/, https://www.agweb.com/"

        return prompt


    def get_client(self):
        return OpenAI(api_key=self.api_key)
    
    def create_assistant(self):
        assistant = self.client.beta.assistants.create(
            name="HarvestIQ Agriculture Agent",
            instructions="You are an expert in agriculture, weather forecasting, and farming practices. Your task is to provide farmers with accurate weather forecasts, planting recommendations, and agricultural advice based on their location and needs. Focus on practical, actionable insights for farming activities.",
            tools=[{"type": "retrieval"}],
            model="gpt-5-nano",
        )
        thread = self.client.beta.threads.create()
        return assistant, thread


    def generate_response(self, user_data, api_key):
        prompt = self.create_openai_assistant_prompt(user_data)
        try:
            response = self.client.chat.completions.create(model="gpt-5-nano", messages=[{"role": "assistant", "content": prompt}])
            return response.choices[0].message.content
        except Exception as e:
            import streamlit as st
            # Try to extract 'input' from error response
            input_msg = None
            try:
                # If error is from openai.BadRequestError, it may have a response attribute
                if hasattr(e, 'response') and e.response is not None:
                    error_json = e.response.json()
                    input_msg = error_json.get('error', {}).get('message', '')
                    # Try to extract 'input' from the message string if present
                    import re, json
                    match = re.search(r"'input': '([^']+)'", input_msg)
                    if match:
                        input_msg = match.group(1)
                    else:
                        # Try to parse message as JSON list and extract 'input'
                        try:
                            msg_list = json.loads(input_msg.replace("'", '"'))
                            if isinstance(msg_list, list) and 'input' in msg_list[0]:
                                input_msg = msg_list[0]['input']
                        except Exception:
                            pass
                else:
                    # Fallback: try to extract 'input' from string
                    import re
                    match = re.search(r"'input': '([^']+)'", str(e))
                    if match:
                        input_msg = match.group(1)
            except Exception:
                input_msg = None
            if input_msg:
                st.error(input_msg)
                return input_msg
            else:
                st.error(f"OpenAI Error: {str(e)}")
                return f"Error: {str(e)}"

            
    
    def chat(self, messages):
        response = self.client.chat.completions.create(model="gpt-5-nano", messages=messages)
        return response.choices[0].message.content
    
    def get_weather(self, location="", longitude="", latitude=""):
        prompt = f"Get the weather forecast for location: {location} or latitude: {latitude}, longitude: {longitude} in python dictionary format only. Do not provide any other text. No intro text. No description. "
        prompt += '''Here is an example for the format:  
                    { 
                    "weather": {
                        "location": "New York",
                        "temperature": 75,
                        "condition": "Sunny",
                        "humidity": 50,
                        "wind_speed": 10,
                        "forecast": ["Sunny", "Cloudy", "Rainy"]
                    }
                }
                 '''
        response = self.client.chat.completions.create(model="gpt-5-nano", messages=[{"role": "assistant", "content": prompt}])

        return response.choices[0].message.content

    def get_planting_time(self, location="", longitude="", latitude=""):
        prompt = f"Get the best planting time for location: {location} or latitude: {latitude}, longitude: {longitude} in python dictionary format only. Do not provide any other text. No intro text. No description. "
        prompt += '''Here is an example for the format:  
                    { 
                    "planting_time": {
                        "location": "New York",
                        "time": "Spring",
                        "crops": ["Tomatoes", "Peppers", "Eggplants"]
                    }
                }
                 '''
        response = self.client.chat.completions.create(model="gpt-5-nano", messages=[{"role": "assistant", "content": prompt}])

        return response.choices[0].message.content

    def get_rain_prediction(self,location="", longitude="", latitude=""):
        # prediction for one week
        prompt = f"Get the rain prediction for location: {location} or latitude: {latitude}, longitude: {longitude} in python dictionary format only. Do not provide any other text. No intro text. No description. "
        prompt += '''Here is an example for the format:  
                    { 
                    "rain_prediction": {
                        "location": "New York",
                        "chance_of_rain": 80,
                        "amount": "10mm",
                        "forecast": ["Rain", "Thunderstorms"],
                        "best_days_to_plant": ["Saturday", "Sunday"],
                        "best_days_to_avoid": ["Monday", "Tuesday"]
                    }
                }
                 '''
        response = self.client.chat.completions.create(model="gpt-5-nano", messages=[{"role": "assistant", "content": prompt}])

        return response.choices[0].message.content

    def text_to_speech(self, text, voice):
        speech_file_path = Path("audio.mp3")
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        response.stream_to_file(speech_file_path)

    def transcribe(self, audio_path):
        audio_file= open(audio_path, "rb")

        transcription = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )

        return transcription.text
