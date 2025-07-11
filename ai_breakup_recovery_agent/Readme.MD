# 💔 Breakup Recovery Agent Team

**Breakup Recovery Agent Team** is an AI-powered application designed to help users emotionally recover from breakups by offering support, emotional release, structured routines, and no-nonsense feedback — all from a team of specialized AI agents.

The app is built using **Streamlit** and **Agno**, and it leverages **Gemini 2.0 Flash (Google Vision Model)** for both text and chat image analysis.

---

## 🚀 Features

### 🧠 Multi-Agent Team:
- **Therapist Agent**: Offers empathetic support and coping strategies.
- **Closure Agent**: Writes emotional messages you shouldn't send — for catharsis.
- **Routine Planner Agent**: Suggests structured routines to aid recovery.
- **Brutal Honesty Agent**: Gives direct, no-fluff insights on your breakup.

### 📷 Chat Screenshot Analysis:
- Upload screenshots of your chats (PNG, JPG, JPEG).
- Get emotional and contextual analysis powered by Google Gemini Vision.

### 🔑 API Key Management:
- Securely manage your Gemini API Key using Streamlit’s sidebar.

### ⚡ Parallel Execution:
- All agents process inputs simultaneously in a coordination mode to provide comprehensive support.

### ✅ User-Friendly Interface:
- Clean, intuitive UI using Streamlit.
- Results neatly displayed agent-by-agent.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **AI Models**: Gemini 2.0 Flash (Google Vision Model)
- **Image Processing**: PIL (Python Imaging Library)
- **Text Extraction**: Google Gemini Vision (for analyzing screenshots)
- **State Management**: `st.session_state` (Streamlit)

---

## 📦 Installation

### Clone the Repository:
```bash
git clone <repository_url>
cd breakup-recovery-agent-team
```
### Create a Virtual Environment (Recommended):
```bash
python -m venv venv
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Run the App:
```bash
streamlit run app.py
```
---

## 🔑 Environment Variables
### Make sure to provide your Gemini API key in the Streamlit sidebar:

```bash
GEMINI_API_KEY=your_google_gemini_api_key
```

## 🛠️ Usage

### 🧭 How to Use

1. **Enter Your Feelings**  
   - Type how you're currently feeling into the text input box provided in the UI.

2. **Upload Screenshot (Optional)**  
   - Upload a screenshot of your chat (PNG, JPG, or JPEG) if you want a visual analysis of the conversation.

3. **Execute Agents**  
   - Click the `Get Recovery Support` button to trigger all AI agents.

4. **View Results**  
   - Each agent's response will be displayed separately.
   - A final summary will be provided by the **Team Leader Agent** for overall guidance.
