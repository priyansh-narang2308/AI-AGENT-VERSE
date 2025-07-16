# AI Music Generator using ModelsLab

### This is a Streamlit-based application that allows users to generate music using the ModelsLab API and Gemini's gemini-1.5-pro model. Users can input a prompt describing the type of music they want to generate, and the application will generate a music track in MP3 format based on the given prompt.

## Features

- Generate Music: Enter a detailed prompt for music generation (genre, instruments, mood, etc.), and the app will generate a music track.
- MP3 Output: The generated music will be in MP3 format, available for listening or download.
- User-Friendly Interface: Simple and clean Streamlit UI for ease of use.
- API Key Integration: Requires both Gemini and ModelsLab API keys to function. API keys are entered in the sidebar for authentication.

## Setup

### Requirements

### 1. API Keys:

- Gemini API Key: Sign up at Google to obtain your API key.
- ModelsLab API Key: Sign up at ModelsLab to get your API key.

### 2. Python 3.8+: Ensure you have Python 3.8 or higher installed.


### Installation

### 1. Clone this repository:
```bash
git clone https://github.com/priyansh-narang2308/AI-AGENT-VERSE
cd ai_music_generator
```

### 2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Running the App

### 1. Start the Streamlit app:
```bash
streamlit run music_generator_agent.py
```

### 2. In the app interface:

- Enter a music generation prompt
- Click "Generate Music"
- Play the music & Download it.
