import os
from uuid import uuid4
from agno.agent import Agent
from agno.models.google import Gemini  
from agno.tools.eleven_labs import ElevenLabsTools
from agno.tools.firecrawl import FirecrawlTools
from agno.agent import Agent, RunResponse
from agno.utils.audio import write_audio_to_file
from agno.utils.log import logger
import streamlit as st

st.set_page_config(page_title="Blog to Podcast Agent", page_icon="🎙️")
st.title("🎙️ Blog to Podcast Agent")

st.sidebar.header("🔑 API Keys")

gemini_api_key = st.sidebar.text_input("Google Gemini API Key", type="password")
eleven_labs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
firecrawl_api_key = st.sidebar.text_input("Firecrawl API Key", type="password")

keys_provided = all([gemini_api_key.strip(), eleven_labs_api_key.strip(), firecrawl_api_key.strip()])

url = st.text_input("Enter the Blog URL to be converted: ", "")

generate_button = st.button("🎙️ Generate Podcast", disabled=not keys_provided)

if not keys_provided:
    st.warning(
        "Please enter all the required API keys to enable your podcast generation."
    )

if generate_button:
    if url.strip() == "":
        st.warning("Please enter a Blog URL.")
    else:
        # Setting the API keys in the environment
        os.environ["GOOGLE_API_KEY"] = gemini_api_key.strip()  
        os.environ["ELEVEN_LABS_API_KEY"] = eleven_labs_api_key.strip()
        os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key.strip()

        with st.spinner(
            "Processing... Scraping blog, summarizing and generating podcast 🎶"
        ):
            try:
                blog_to_podcastagent = Agent(
                    name="Blog to Podcast Agent",
                    agent_id="blog_to_podcastagent",
                    model=Gemini(id="gemini-1.5-flash"),  
                    tools=[
                        ElevenLabsTools(
                            voice_id="JBFqnCBsd6RMkjVDRZzb",
                            model_id="eleven_multilingual_v2",
                            target_directory="audio_generations",
                        ),
                        FirecrawlTools(),
                    ],
                    description="You are an AI agent that can generate audio using the ElevenLabs API.",
                    instructions=[
                        "When the user provides a blog URL:",
                        "1. Use FirecrawlTools to scrape the blog content",
                        "2. Create a concise summary of the blog content that is NO MORE than 2000 characters long",
                        "3. The summary should capture the main points while being engaging and conversational",
                        "4. Use the ElevenLabsTools to convert the summary to audio",
                        "5. If ElevenLabs API fails, still provide the text summary",
                        "Ensure the summary is within the 2000 character limit to avoid ElevenLabs API limits",
                    ],
                    markdown=True,
                    debug_mode=True,
                )
                
                podcast: RunResponse = blog_to_podcastagent.run(
                    f"Convert the blog content to a podcast: {url}"
                )

                save_dir = "audio_generations"
                os.makedirs(save_dir, exist_ok=True)
                
                if hasattr(podcast, 'content') and podcast.content:
                    st.success("✨ Blog Summary Generated Successfully!")
                    st.write("**Summary:**")
                    st.write(podcast.content)
                
                if hasattr(podcast, 'audio') and podcast.audio and len(podcast.audio) > 0:
                    try:
                        filename = f"{save_dir}/podcast_{uuid4()}.wav"
                        write_audio_to_file(
                            audio=podcast.audio[0].base64_audio,
                            filename=filename
                        )
                        
                        st.success("🎙️ Audio Generated Successfully!")
                        with open(filename, "rb") as f:
                            audio_bytes = f.read()
                        st.audio(audio_bytes, format="audio/wav")
                        
                        st.download_button(
                            label="🎧 Download Podcast",
                            data=audio_bytes,
                            file_name="generated_podcast.wav",
                            mime="audio/wav"
                        )
                    except Exception as audio_error:
                        st.warning(f"Audio generation failed: {str(audio_error)}")
                        st.info("But the text summary above was generated successfully!")
                else:
                    st.warning("No audio was generated (likely due to ElevenLabs API issues), but text summary is available above.")
                    st.info("💡 **Tip**: Try getting a paid ElevenLabs subscription to avoid API restrictions.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Streamlit app error: {str(e)}")
                
                st.info("**Debug Info:**")
                st.write("- Make sure you're using the correct API keys")
                st.write("- Check that your Google API key is from Google AI Studio")
                st.write("- Verify your ElevenLabs API key is valid and not rate-limited")
                st.write("- Ensure your Firecrawl API key is active")