# HarvestIQ - AI-Powered Smart Agriculture Advisor

HarvestIQ is an AI-powered smart agriculture advisor designed to support farmers worldwide, with special focus on African agriculture. By combining local farming knowledge with cutting-edge AI, HarvestIQ delivers accurate weather forecasts, rain predictions, and personalized crop planting recommendations.

## 🌱 Features

- **Weather Outlook**: Real-time weather forecasts tailored to specific locations
- **Best Planting Times**: Optimal planting schedules based on historical weather data
- **Rain Prediction**: Advanced rainfall predictions for proactive farming planning
- **Personalized Advice**: AI-generated recommendations based on user location and needs
- **Audio Responses**: Text-to-speech functionality for accessibility

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd HarvestIQ
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key in the application sidebar

### Running the Application

```bash
streamlit run app.py
```

## 📋 Usage

1. **Provide Your Information**: Fill out the questionnaire with your location details
2. **Get Weather Forecasts**: Receive detailed weather outlook for your area
3. **Plan Planting**: Get optimal planting times and crop recommendations
4. **Predict Rainfall**: Stay ahead of weather changes with rain predictions

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI**: OpenAI GPT models
- **Audio**: OpenAI Text-to-Speech
- **Data Processing**: Pandas, PyDeck

## 📁 Project Structure

```
HarvestIQ/
├── app.py              # Main application
├── assistant.py        # AI assistant functionality
├── information.py      # User data collection
├── response.py         # Response handling
├── weather.py          # Weather-specific features
├── style.css          # Custom styling
├── requirements.txt   # Dependencies
└── assets/            # Image assets
```

## 🌍 Mission

Our mission is to bridge technology and tradition, helping farmers boost productivity, reduce risks, and make data-driven decisions while honoring cultural farming practices.

## 📞 Support

For support or questions, please refer to the application's help section or contact our team.

## 📄 License

This project is licensed for agricultural and educational purposes.
