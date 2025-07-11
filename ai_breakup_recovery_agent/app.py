from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Image as AgnoImage
from agno.tools.duckduckgo import DuckDuckGoTools
import streamlit as st
from typing import List, Optional
import logging
from pathlib import Path
import tempfile
import os

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def initialize_agents(api_key: str) -> tuple[Agent, Agent, Agent, Agent]:
    try:
        model = Gemini(id="gemini-1.5-pro", api_key=api_key)

        therapy_agent = Agent(
            model=model,
            name="AI Breakup Therapist Agent",
            instructions=[
                "You are an empathetic therapist that:",
                "1. Listens with empathy and validates feelings",
                "2. Uses gentle humor to lighten the mood",
                "3. Shares relatable breakup experiences",
                "4. Offers comforting words and encouragement",
                "5. Analyzes both text and image inputs for emotional context",
                "Be supportive and understanding in your responses",
            ],
            markdown=True,
        )

        emotion_agent = Agent(
            model=model,
            name="Emotion Agent",
            instructions=[
                "You are a closure specialist that:",
                "1. Creates emotional messages for unsent feelings",
                "2. Helps express raw, honest emotions",
                "3. Formats messages clearly with headers",
                "4. Ensures tone is heartfelt and authentic",
                "Focus on emotional release and closure",
            ],
            markdown=True,
        )

        routine_planner_agent = Agent(
            model=model,
            name="Routine Planner Agent",
            instructions=[
                "You are a recovery routine planner that:",
                "1. Designs 7-day recovery challenges",
                "2. Includes fun activities and self-care tasks",
                "3. Suggests social media detox strategies",
                "4. Creates empowering playlists",
                "Focus on practical recovery steps",
            ],
            markdown=True,
        )

        brutal_honesty_agent = Agent(
            model=model,
            name="Brutal Honesty Agent",
            tools=[DuckDuckGoTools()],
            instructions=[
                "You are a direct feedback specialist that:",
                "1. Gives raw, objective feedback about breakups",
                "2. Explains relationship failures clearly",
                "3. Uses blunt, factual language",
                "4. Provides reasons to move forward",
                "Focus on honest insights without sugar-coating",
            ],
            markdown=True
        )
        
        return therapy_agent,emotion_agent,routine_planner_agent,brutal_honesty_agent

    except Exception as e:
        st.error("Error initializing agents: " + str(e))
        return None, None, None, None


# this is to set the page config and the ui of the page
st.set_page_config(
    page_title="AI Breakup Recovery Agent",
    page_icon="💔",
    layout="wide"
)

# the side bar for the api key
with st.sidebar:
    st.header("🔑 API Configuration")
    
    if "api_key_input" not in st.session_state:
        st.session_state.api_key_input = ""
        
    api_key = st.text_input(
        "Enter your Gemini API Key",
        value=st.session_state.api_key_input,
        type="password",
        help="Get your API key from Google AI Studio",
        key="api_key_widget"  
    )
    
    if api_key != st.session_state.api_key_input:
        st.session_state.api_key_input = api_key
    
    if api_key:
        st.success("API Key provided! ✅")
    else:
        st.warning("Please enter your API key to proceed")
        st.markdown("""
        To get your API key:
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Enable the Generative Language API in your [Google Cloud Console](https://console.developers.google.com/apis/api/generativelanguage.googleapis.com)
        """)
        

# mAIN cONTENT
st.title("❤️‍🩹 Breakup Recovery Squad")
st.markdown("""
    ### Your AI-powered breakup recovery team is here to help!
    Share your feelings and chat screenshots, and we'll help you navigate through this tough time.
""")

# this is the input section
col1,col2=st.columns(2)

with col1:
    st.subheader("Share Your Feelings!")
    user_input=st.text_area(
        "How are you feeling? What bad has happened with you?",
        height=150,
        placeholder="Tell us your story..."
        )
    
with col2:
    st.subheader("Upload Chat Screenshots Here")
    uploaded_files=st.file_uploader(
        "Upload screenshots of your chats (optional)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="screenshots"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            st.image(file,caption=file.name,use_container_width=True)
            

# now main part the process button
if st.button("Get Recovery Plan 💝",type="primary"):
    if not st.session_state.api_key_input:
        st.warning("Please enter your API key in the sidebar first!")   
    else:
        therapy_agent,emotion_agent,routine_planner_agent, brutal_honesty_agent=initialize_agents(st.session_state.api_key_input)
        
        if all([therapy_agent,emotion_agent,routine_planner_agent,brutal_honesty_agent]):
            if user_input or uploaded_files:
                try:
                    st.header("Your Personalized Recovery Plan")
                    
                    def process_images(files):
                        processed_images = []
                        for file in files:
                            try:
                                temp_dir = tempfile.gettempdir()
                                temp_path = os.path.join(temp_dir, f"temp_{file.name}")
                                
                                with open(temp_path, "wb") as f:
                                    f.write(file.getvalue())
                                
                                agno_image = AgnoImage(filepath=Path(temp_path))
                                processed_images.append(agno_image)
                                
                            except Exception as e:
                                logger.error(f"Error processing image {file.name}: {str(e)}")
                                continue
                        return processed_images
                    
                    all_images = process_images(uploaded_files) if uploaded_files else []
                    
                    # this is for the therapist agent to get hte therapy ok
                    with st.spinner("🤗 Getting empathetic support..."):
                        therapist_prompt = f"""
                        Analyze the emotional state and provide empathetic support based on:
                        User's message: {user_input}
                        
                        Please provide a compassionate response with:
                        1. Validation of feelings
                        2. Gentle words of comfort
                        3. Relatable experiences
                        4. Words of encouragement
                        """
                        
                        response = therapy_agent.run(
                            message=therapist_prompt,
                            images=all_images
                        )
                        
                        st.subheader("🤗 Emotional Support")
                        st.markdown(response.content)
                        
                        # to make emotinasl mesges
                    with st.spinner("✍️ Crafting emotion messages..."):
                        emotion_prommpt=f"""
                            Help create emotional closure based on:
                        User's feelings: {user_input}
                        
                        Please provide:
                        1. Template for unsent messages
                        2. Emotional release exercises
                        3. Closure rituals
                        4. Moving forward strategies
                        """
                        
                        response = emotion_agent.run(
                            message=emotion_prommpt,
                            images=all_images
                        )
                        
                        st.subheader("✍️ Finding Emotions")
                        st.markdown(response.content)
                        
                        # to make a recovery plan
                    with st.spinner("📅 Creating your recovery plan..."):
                        reocbvery_prompt=f"""
                            Design a 7 day recovery plan based on:
                            Current state:{user_input}
                            
                            Include :
                             1. Daily activities and challenges
                        2. Self-care routines
                        3. Social media guidelines
                        4. Mood-lifting music suggestions
                        """
                        
                        response=routine_planner_agent.run(
                            message=reocbvery_prompt,
                            images=all_images
                        )
                        
                        st.subheader("📅 Your Recovery Plan")
                        st.markdown(response.content)
                        
                        # this is for gettng honest repsone
                    with st.spinner("💪 Getting honest perspective..."):
                        honesty_prompt = f"""
                        Provide honest, constructive feedback about:
                        Situation: {user_input}
                        
                        Include:
                        1. Objective analysis
                        2. Growth opportunities
                        3. Future outlook
                        4. Actionable steps
                        """
                        
                        response = brutal_honesty_agent.run(
                            message=honesty_prompt,
                            images=all_images
                        )
                        
                        st.subheader("💪 Honest Perspective")
                        st.markdown(response.content)
                       
                    
                except Exception as e:
                    logger.error(f"Error during analysis: {str(e)}")
                    st.error("An error occurred during analysis. Please check the logs for details.")
            
            else:
                st.warning("Please share your feelings or upload screenshots to get help.")
        else:
            st.error("Failed to initialize agents. Please check if your API key is provided!")
            
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Made with ❤️ by Priyansh for recovery comeback</p>
    </div>
""", unsafe_allow_html=True)
