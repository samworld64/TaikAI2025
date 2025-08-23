
from openai import OpenAI
from pathlib import Path
import streamlit as st
import requests
import datetime


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

        if user_data['target'] == 'weather':
            location = user_data.get('location', '')
            prompt = f"Create a comprehensive 7-day agricultural weather forecast for {location}. "
            prompt += '''\nProvide a structured table with the following columns:\n- Day/Date\n- Temperature Range (High/Low)\n- Weather Conditions\n- Humidity Level\n- Wind Speed\n- Precipitation Chance\n- Farmer-Specific Recommendations'''
            prompt += "\nInclude actionable insights for farming activities based on typical weather patterns for this region and time of year."
            prompt += f"\nCurrent time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        elif user_data['target'] == 'planting_time':
            prompt = f"Get the best planting time for location: {user_data.get('location', '')} or latitude: {user_data.get('latitude', '')}, longitude: {user_data.get('longitude', '')}. Provide for the whole year, starting from now. "
            prompt += '''\nDetails to provide:\n- location\n- crops recommended\n- time recommended\n- weather forecast\n'''
            prompt += "\nTask: Recommend optimal planting times and crops for the user's area, based on local climate and agricultural best practices."
            prompt += "\nRestrict your sources to reliable agricultural resources such as https://www.agronomy.org/, https://www.cimmyt.org/, https://www.fao.org/"
        elif user_data['target'] == 'prediction':
            location = user_data.get('location', '')
            prompt = f"Create a rain prediction and farming guidance template for {location} based on typical weather patterns for this region. "
            prompt += '''\nProvide a structured response with:\n- Likelihood of rain today\n- Expected rainfall amount\n- Weather conditions forecast\n- Best times for planting activities\n- Times to avoid outdoor work'''
            prompt += "\nInclude specific farming recommendations based on typical weather patterns for this region."
            prompt += f"\nCurrent time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        return prompt


    def get_client(self):
        return OpenAI(api_key=self.api_key)
    
    def create_assistant(self):
        assistant = self.client.beta.assistants.create(
            name="HarvestIQ Agriculture Agent",
            instructions="You are an expert in agriculture and farming practices. Your task is to interact with users to collect location and farming information. Use this information to provide tailored advice on weather forecasts, optimal planting times, crop recommendations, and agricultural best practices. Focus on sustainable farming and helping farmers make data-driven decisions. Use web browsing capabilities to search for the most current weather data and agricultural information.",
            tools=[{"type": "retrieval"}, {"type": "web_browser"}],
            model="gpt-5-nano",
        )
        thread = self.client.beta.threads.create()
        return assistant, thread


    def generate_response(self, user_data, api_key):
        prompt = self.create_openai_assistant_prompt(user_data)
        st.info("Searching for the most recent available information...")  # Real-time feedback to the user
        try:
            response = self.client.chat.completions.create(model="gpt-5-nano", messages=[{"role": "assistant", "content": prompt}])
            result = response.choices[0].message.content
            
            # Add timestamp information to the response
            import datetime
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Check if the response indicates missing or incomplete data
            if any(phrase in result.lower() for phrase in ["unable to find", "no data available", "could not retrieve", "not available"]):
                result += f"\n\nNote: Using the most recent data available as of {current_time}. Some information may not be current."
            else:
                result += f"\n\nData retrieved as of {current_time}."
            
            return result
        except Exception as e:
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
    
    def get_agriculture_services(self, zip_code):
        prompt = f"Provide longitude and latitude of local agriculture services and farming supply stores in the area of the zipcode {zip_code} in python dictionary format only. Do not provide any other text. No intro text. No description. "
        prompt += '''Here is an example for the format:  
                    { 
                    "agriculture_services": [
                        {
                            "name": "Local Farming Supply Store",
                            "lat": 37.7749,
                            "lon": -122.4194,
                            "services_offered": ["Seeds", "Fertilizers", "Farming Tools"],
                        }
                    ]}
                 '''
        response = self.client.chat.completions.create(model="gpt-5-nano", messages=[{"role": "assistant", "content": prompt}])

        return response.choices[0].message.content
    def get_live_weather_data(self, location="", latitude="", longitude=""):
        """Fetch live weather data from a weather API"""
        import requests
        
        # You can replace this with any weather API of your choice
        # Example using OpenWeatherMap (requires API key)
        api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with your actual API key
        
        # Try to get coordinates if available
        if latitude and longitude:
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        elif location:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        else:
            return {"error": "No location or coordinates provided"}
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            weather_data = response.json()
            
            # Format the response
            formatted_data = {
                "location": weather_data.get("name", location),
                "temperature": weather_data["main"]["temp"],
                "condition": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"],
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return formatted_data
        except Exception as e:
            return {"error": str(e), "message": "Could not retrieve live weather data"}

    def get_weather(self, location="", longitude="", latitude=""):
        return self.get_live_weather_data(location, latitude, longitude)

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
        
        # Truncate text to 4096 characters to avoid OpenAI TTS limits
        if len(text) > 4096:
            text = text[:4090] + "..."  # Leave room for ellipsis
        
        # Clean text to handle Unicode characters properly
        # Replace problematic Unicode characters with ASCII equivalents
        text = text.replace('\u2019', "'")  # Right single quotation mark
        text = text.replace('\u2018', "'")  # Left single quotation mark
        text = text.replace('\u201c', '"')  # Left double quotation mark
        text = text.replace('\u201d', '"')  # Right double quotation mark
        text = text.replace('\u2013', '-')  # En dash
        text = text.replace('\u2014', '-')  # Em dash
        
        # Remove any other non-ASCII characters that might cause issues
        text = text.encode('utf-8', 'ignore').decode('utf-8')
        
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            response.stream_to_file(speech_file_path)
        except Exception as e:
            print(f"Error in text-to-speech conversion: {e}")
            # Fallback: create a simple error message audio
            fallback_text = "Weather forecast information is available."
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=fallback_text
            )
            response.stream_to_file(speech_file_path)

    def transcribe(self, audio_path):
        audio_file= open(audio_path, "rb")

        transcription = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )

        return transcription.text
