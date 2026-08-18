import os
from datetime import datetime
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# Load API key from .env file (optional - user can also paste manually)
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Page configuration
st.set_page_config(page_title="AI Study & Meeting Assistant", page_icon="🧠", layout="wide")

# ==========================================
# SIDEBAR: API Key Configuration
# ==========================================
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("Enter your DeepSeek API key below. It will **not** be stored or saved anywhere.")
    
    api_key = st.text_input("DeepSeek API Key", type="password", placeholder="Enter your API key here...")
    
    if not api_key:
        st.warning("⚠️ Please enter your DeepSeek API key to use the assistant.")
    else:
        st.success("✅ API key configured (not stored)")
    
    st.markdown("---")
    st.caption("💡 **Responsible AI Practice:** Always verify AI-generated facts against trusted sources. Your API key stays local and is never stored.")

# ==========================================
# MAIN APP: Two Tabs
# ==========================================
st.title("🧠 AI Study & Meeting Assistant")
st.markdown("Choose a tool below:")

tab1, tab2 = st.tabs(["📚 Study Assistant", "📋 Meeting Minutes Assistant"])

# ==========================================
# TAB 1: STUDY ASSISTANT
# ==========================================
with tab1:
    st.header("📚 Study Assistant")
    st.markdown("Enter a topic or paste your notes to get a summary and practice questions.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sample study topics
        sample_topic = """Photosynthesis is the process by which plants, algae, and some bacteria convert light energy into chemical energy stored in glucose. It occurs in the chloroplasts, primarily in the leaves. The process uses carbon dioxide, water, and sunlight to produce glucose and oxygen. There are two main stages: the light-dependent reactions and the Calvin cycle (light-independent reactions). Chlorophyll is the pigment responsible for capturing light energy."""
        
        study_input = st.text_area(
            "Enter your topic or paste your notes:",
            height=300,
            value=sample_topic,
            help="Replace this with your own topic or notes."
        )
        
        # Quick topic buttons
        st.markdown("**Quick topics:**")
        quick_topics = ["Photosynthesis", "French Revolution", "Machine Learning", "Python Basics"]
        cols = st.columns(len(quick_topics))
        for i, topic in enumerate(quick_topics):
            if cols[i].button(topic, key=f"study_{topic}"):
                study_input = topic
        
        if st.button("📝 Clear", key="clear_study"):
            study_input = ""
            st.rerun()
    
    with col2:
        st.subheader("📊 AI-Generated Study Material")
        
        if st.button("🚀 Generate Study Material", key="study_generate", type="primary"):
            if not study_input.strip():
                st.error("❌ Please enter a topic or notes first.")
            elif not api_key:
                st.error("❌ Please enter your DeepSeek API key in the sidebar.")
            else:
                with st.spinner("🤖 Generating summary and practice questions..."):
                    try:
                        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                        
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {"role": "system", "content": """You are a helpful study assistant.
Given the topic or notes, do the following:
1. Write a 1-paragraph summary
2. Generate 5 practice questions with answers
3. Format your response clearly with labels: "Summary:", "Question 1:", etc.
If you are unsure about a fact, say 'Uncertain' instead of inventing."""},
                                {"role": "user", "content": study_input}
                            ],
                            temperature=0.7,
                            max_tokens=1000
                        )
                        
                        result = response.choices[0].message.content
                        
                        st.markdown("### ✅ Study Material Generated!")
                        st.markdown(result)
                        
                        # Download button
                        if st.download_button(
                            label="📥 Download Study Material",
                            data=result,
                            file_name=f"study_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            key="study_download"
                        ):
                            st.success("✅ File downloaded!")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                        st.info("💡 Tips: Check your API key, internet connection, and DeepSeek account balance.")

# ==========================================
# TAB 2: MEETING MINUTES ASSISTANT
# ==========================================
with tab2:
    st.header("📋 Meeting Minutes Assistant")
    st.markdown("Upload your meeting notes and get AI-generated action points, tasks, and next steps.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sample_meeting = """Date: August 17, 2024
Attendees: Project Team (Alice, Bob, Carol)
Agenda: Weekly Project Review

Discussion:
- Alice presented the Q3 progress report. The team is 80% complete with Phase 1.
- Bob noted that the design team needs the final requirements by Friday.
- Carol identified a potential risk with the vendor delivery timeline.
- We discussed the need for a backup plan if the vendor is delayed.

Decisions:
- Q4 budget will be allocated next week
- Design team will get requirements by Friday
- We need a backup vendor identified by next Monday

Action Items:
- Alice: Finalize Q3 report and share by EOD Thursday
- Bob: Finalize design requirements and send to design team by Friday COB
- Carol: Research backup vendors and present options on Monday
- Team: Schedule weekly sync for next Wednesday

My Tasks:
- Schedule the meeting for next Wednesday
- Follow up with Alice on Thursday morning about the report
- Send a reminder to Bob about Friday's deadline
- Create a shared document for vendor backup options"""
        
        meeting_notes = st.text_area(
            "Paste your meeting minutes below:",
            height=400,
            value=sample_meeting,
            help="Replace this with your actual meeting notes or upload a file."
        )
        
        uploaded_file = st.file_uploader("Or upload a text file", type=["txt", "md"])
        
        if uploaded_file is not None:
            meeting_notes = uploaded_file.read().decode("utf-8")
            st.text_area("File content:", meeting_notes, height=200, key="meeting_file_preview")
        
        if st.button("📝 Clear", key="clear_meeting"):
            meeting_notes = ""
            st.rerun()
    
    with col2:
        st.subheader("📊 AI Analysis")
        
        if st.button("🚀 Generate Analysis", key="meeting_generate", type="primary"):
            if not meeting_notes.strip():
                st.error("❌ Please enter some meeting notes first.")
            elif not api_key:
                st.error("❌ Please enter your DeepSeek API key in the sidebar.")
            else:
                with st.spinner("🤖 Analyzing meeting notes..."):
                    try:
                        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                        
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {"role": "system", "content": """You are a professional meeting assistant.
Given the meeting minutes, do the following in a clear, structured format:

1. **Summary**: Write a 2-3 sentence summary of the meeting
2. **Key Decisions**: List the key decisions made (bullet points)
3. **Action Points**: List all action items with:
   - What needs to be done
   - Who is responsible (if mentioned)
   - Deadline (if mentioned)
4. **My Tasks**: Identify ALL tasks that are specifically for the note-taker (the person who wrote the notes)
5. **Process/Next Steps**: Describe what needs to happen next

If something is unclear, state "Uncertain" instead of inventing."""},
                                {"role": "user", "content": meeting_notes}
                            ],
                            temperature=0.7,
                            max_tokens=1500
                        )
                        
                        result = response.choices[0].message.content
                        
                        st.markdown("### ✅ Analysis Complete")
                        st.markdown(result)
                        
                        if st.download_button(
                            label="📥 Download Analysis",
                            data=result,
                            file_name=f"meeting_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            key="meeting_download"
                        ):
                            st.success("✅ File downloaded!")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                        st.info("💡 Tips: Check your API key, internet connection, and DeepSeek account balance.")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.caption("🧠 Built with Streamlit + DeepSeek API | 💡 Always verify AI-generated content")