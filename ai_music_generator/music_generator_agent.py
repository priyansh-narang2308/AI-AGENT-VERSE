import os
from uuid import uuid4
import requests
from agno.agent import Agent,RunResponse
from agno.models.google import Gemini
from agno.tools.models_labs import FileType, ModelsLabTools
from agno.utils.log import logger
import streamlit as st

st.sidebar.title("API Key Configuration")

gemini_api_key=st.sidebar.text_input("Enter your Gemini API Key",type="password")
models_labs_api_key=st.sidebar.text_input("Enter your ModelsLab API Key",type="password")

st.set_page_config(page_title="AI Music Generator",page_icon="🎵")
st.title("🎶 AI Music Generator")
prompt = st.text_area("Enter a music generation prompt:", "Generate a 30 second classical music piece", height=100)

if gemini_api_key and models_labs_api_key:
    agent=Agent(
        name="AI Music Generator",
        agent_id="ml_music_agent",
        model=Gemini(id="gemini-1.5-pro",api_key=gemini_api_key),
        show_tool_calls=True,
        tools=[ModelsLabTools(api_key=models_labs_api_key, wait_for_completion=True, file_type=FileType.MP3)],
        description="You are an AI agent that can generate music using the ModelsLabs API.",
        instructions=[
            "When generating music, use the `generate_media` tool with detailed prompts that specify:",
            "- The genre and style of music (e.g., classical, jazz, electronic)",
            "- The instruments and sounds to include",
            "- The tempo, mood and emotional qualities",
            "- The structure (intro, verses, chorus, bridge, etc.)",
            "Create rich, descriptive prompts that capture the desired musical elements.",
            "Focus on generating high-quality, complete instrumental pieces.",
        ],
        markdown=True,
        debug_mode=True,
    )
    
    if st.button("✨ Generate Music"):
        if prompt.strip()=="":
            st.warning("Please enter a music prompt first.")
        else:
            with st.spinner("Generating Music..."):
                try:
                    music:RunResponse=agent.run(prompt)
                    if music.audio and len(music.audio)>0:
                        save_directiry="audio_generations"
                        os.makedirs(save_directiry,exist_ok=True)
                        
                        url=music.audio[0].url
                        resp=requests.get(url)
                        
                        #this to validtte the repsonse
                        if not resp.ok:
                            st.error(f"Failed to download audio. Status code: {resp.status_code}")
                            st.stop()
                            
                        content_type = resp.headers.get("Content-Type", "")
                        if "audio" not in content_type:
                            st.error(f"Invalid file type returned: {content_type}")
                            st.write(" Debug: Downloaded content was not an audio file.")
                            st.write("URL:", url)
                            st.stop()
                            
                        #this saves the audio
                        filename = f"{save_directiry}/music_{uuid4()}.mp3"
                        with open(filename, "wb") as f:
                            f.write(resp.content)    
                            
                        #this plaeys the audio
                        st.success("Music Generated Successfully 🎉")  
                        audio_bits=open(filename,"rb").read()
                        st.audio(audio_bits, format="audio/mp3")
                        
                        st.download_button(
                            label="Download Music",
                            data=audio_bits,
                            file_name="generated_music.mp3",
                            mime="audio/mp3"
                        )
              
                    else:
                        st.error("No audio generated. Please try again.")
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    logger.error(f"Streamlit app error: {e}")
                    
else:
    st.sidebar.warning("Please enter both the Gemini and ModelsLab API keys to use the app.")