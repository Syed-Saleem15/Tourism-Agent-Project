# ✈️ Tourism AI Agent

A multi-agent tourism system that provides weather information and tourist attraction recommendations using a clean, modular architecture.

## 🌟 Features

- **Multi-Agent Architecture**: Parent agent orchestrates specialized child agents
- **Weather Information**: Real-time weather and 3-day forecast via Open-Meteo API
- **Tourist Attractions**: Discover up to 5 nearby attractions via Overpass API
- **Smart Intent Detection**: Automatically understands what information you need
- **Location Geocoding**: Converts place names to coordinates using Nominatim API
- **Clean UI**: Beautiful, responsive Streamlit interface
- **Error Handling**: Graceful handling of API failures and invalid locations

## 📁 Project Structure

```
tourism_agent_project/
│
├── agents/
│   ├── __init__.py             # Package initializer
│   ├── parent_agent.py         # Tourism AI orchestrator
│   ├── weather_agent.py        # Weather API integration
│   └── places_agent.py         # Tourist attractions API integration
│
├── ui/
│   └── app.py                  # Streamlit web interface
│
├── utils/
│   ├── __init__.py             # Package initializer
│   └── api_helpers.py          # Shared API utilities
│
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .gitignore                  # Git ignore file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for API calls)

### Installation

1. **Clone or download the project**
   ```bash
   cd tourism_agent_project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

1. **Start the application**
   ```bash
   streamlit run ui/app.py
   ```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to that URL manually

3. **Start using the app**
   - Enter a query like "I'm going to Paris, let's plan my trip"
   - Get weather information and tourist attractions instantly!

## 💡 Usage Examples

### Example Queries

1. **Get tourist attractions only:**
   ```
   I'm going to Bangalore, let's plan my trip
   ```

2. **Get weather information:**
   ```
   What's the weather in Tokyo?
   I'm going to London, what is the temperature there?
   ```

3. **Get both weather and attractions:**
   ```
   I'm visiting New York, what is the temperature there and what are the places I can visit?
   Tell me about Paris weather and tourist spots
   ```

### Expected Behavior

- **Valid location**: Returns weather and/or attractions based on your query
- **Invalid location**: Shows error message "I'm sorry, I don't know this place exists"
- **Ambiguous query**: Defaults to showing tourist attractions

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free)

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file path: `ui/app.py`
   - Click "Deploy"

### Deploy to Hugging Face Spaces (Free)

1. **Create a new Space**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Select "Streamlit" as SDK

2. **Upload files**
   - Upload all project files
   - Ensure `requirements.txt` is in root directory
   - Set app file to `ui/app.py` in Space settings

3. **Environment variables** (if needed)
   - No API keys required - all APIs are free and public

## 🔧 Technical Details

### APIs Used

1. **Open-Meteo API**
   - Endpoint: `https://api.open-meteo.com/v1/forecast`
   - No API key required
   - Provides weather and forecast data

2. **Nominatim API (OpenStreetMap)**
   - Endpoint: `https://nominatim.openstreetmap.org/search`
   - No API key required
   - Converts place names to coordinates

3. **Overpass API**
   - Endpoint: `https://overpass-api.de/api/interpreter`
   - No API key required
   - Queries OpenStreetMap for tourist attractions

### Agent Architecture

- **Parent Agent**: Analyzes user intent and coordinates child agents
- **Weather Agent**: Fetches weather data from Open-Meteo
- **Places Agent**: Gets coordinates and finds tourist attractions

## 🛠️ Development

### Adding New Features

1. **Add a new agent:**
   - Create a new file in `agents/` directory
   - Follow the pattern of existing agents
   - Import and integrate in `parent_agent.py`

2. **Modify UI:**
   - Edit `ui/app.py`
   - Use Streamlit components for interactive elements

3. **Add API utilities:**
   - Add helper functions in `utils/api_helpers.py`

### Testing

Run the application locally and test with various queries:
- Valid locations (cities, countries, landmarks)
- Invalid locations (gibberish, typos)
- Different query types (weather only, places only, both)
- Edge cases (small towns, islands, etc.)

## 📝 Notes

- All APIs used are free and don't require authentication
- Rate limits apply to public APIs - use responsibly
- Tourist attractions depend on OpenStreetMap data availability
- Some locations may have limited attraction data

## 🤝 Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available for educational and personal use.

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" error**
   - Ensure you're in the project root directory
   - Verify virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **API timeout errors**
   - Check your internet connection
   - Public APIs may experience temporary downtime
   - The app will retry failed requests automatically

3. **No attractions found**
   - Some locations may have limited OpenStreetMap data
   - Try a larger or more popular city
   - The search radius is 5km by default

4. **Location not recognized**
   - Use common place names (cities, countries)
   - Check spelling
   - Try adding country name (e.g., "Paris, France")

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review example queries
- Ensure all dependencies are installed correctly

---

**Enjoy planning your trips with Tourism AI Agent! ✈️🌍**