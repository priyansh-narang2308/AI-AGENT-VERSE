# Blog to Podcast Agent

### This is a Streamlit-based application that allows users to convert any blog post into a podcast. The app uses Google's gemini-1.5-pro model for summarization, Firecrawl for scraping blog content, and ElevenLabs API for generating audio. Users simply input a blog URL, and the app will generate a podcast episode based on the blog.


## Features

- **Blog Scraping**: Scrapes the full content of any public blog URL using the Firecrawl API.
- **Summary Generation**: Creates an engaging and concise summary of the blog (within 2000 characters) using OpenAI GPT-4.
- **Podcast Generation**: Converts the summary into an audio podcast using the ElevenLabs voice API.
- **API Key Integration**: Requires Gemini, Firecrawl, and ElevenLabs API keys, entered securely via the sidebar.

---

## Setup

### Requirements

#### API Keys:

- **Gemini API Key**: [Get it here](https://aistudio.google.com/apikey)
- **ElevenLabs API Key**: [Get it here](https://www.elevenlabs.io/)
- **Firecrawl API Key**: [Get it here](https://firecrawl.dev/)

#### System Requirements:

- **Python 3.8+**: Make sure Python 3.8 or higher is installed on your system.

### Requirements

## Installation

### 1. Clone this repository:

```bash
git clone https://github.com/priyansh-narang2308/AI-AGENT-VERSE
cd blog_to_podcast
```

### 2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Running the App

### 1. Start the Streamlit app:
```bash
streamlit run blog_to_podcast.py
```

### 2. In the app interface:

- Enter your Gemini, ElevenLabs, and Firecrawl API keys in the sidebar.
- Input the blog URL you want to convert.
- Click "🎙️ Generate Podcast".
- Listen to the generated podcast or download it.