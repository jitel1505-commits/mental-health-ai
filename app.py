import streamlit as st
from model import MentalHealthRiskAnalyzer

# Page configuration
st.set_page_config(
    page_title="MedAI Core - Mental Health Risk Analyzer",
    page_icon="🧠",
    layout="wide"
)

# Initialize AI Model
@st.cache_resource
def load_model():
    return MentalHealthRiskAnalyzer()

analyzer = load_model()

# Sidebar Navigation & Branding
st.sidebar.markdown("## 🧠 MedAI Core")
st.sidebar.markdown("**Active Mode:** Clinical AI Assistant")
st.sidebar.markdown("---")
selected_tab = st.sidebar.radio(
    "Navigation Portal",
    ["Risk Predictor & Symptom Checker", "Journal & Mood History", "Crisis Support & Helplines"]
)

st.sidebar.markdown("---")
st.sidebar.info("⚠️ **Automated Notice:** This tool provides educational guidance and preliminary risk analysis. It does not replace a licensed psychiatrist or clinical diagnosis.")

# Main Header
st.title("Patient Dashboard — Mental Health Risk Analysis")
st.markdown("Provide details about how you are feeling or describe recent emotional patterns to receive structured AI insights.")

if selected_tab == "Risk Predictor & Symptom Checker":
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.subheader("🤖 AI Clinical Mental Health Analyzer")
        user_input = st.text_area(
            "Describe your current feelings, sleep patterns, or emotional state:",
            placeholder="E.g., I have been feeling constantly anxious for 5 days, low energy, and unable to sleep...",
            height=150
        )
        
        # Quick tags for testing
        st.markdown("*(Or select a common emotional concern for instant analysis)*:")
        tag_col1, tag_col2, tag_col3 = st.columns(3)
        if tag_col1.button("Exam Burnout & Stress"):
            user_input = "Feeling completely burned out and stressed about upcoming examinations."
        if tag_col2.button("Persistent Anxiety"):
            user_input = "Constant racing thoughts, worry, and difficulty sleeping every night."
        if tag_col3.button("Severe Hopelessness"):
            user_input = "I feel completely hopeless and don't see any point in continuing."

        if st.button("Analyze Mental Health Risk", type="primary"):
            if user_input.strip() == "":
                st.warning("Please enter a description or select a common concern first.")
            else:
                with st.spinner("Analyzing linguistic patterns and risk factors..."):
                    analysis = analyzer.analyze(user_input)
                    
                    st.session_state['last_analysis'] = analysis
                    st.session_state['last_input'] = user_input

    with col2:
        st.subheader("📊 Patient Care History & Timeline")
        if 'last_analysis' in st.session_state:
            res = st.session_state['last_analysis']
            
            # Color-coded triage banner
            if res['color'] == 'red':
                st.error(f"🔴 **TRIAGE LEVEL: {res['level']}** (Confidence: {res['confidence_score']}%)")
            elif res['color'] == 'orange':
                st.warning(f"🟠 **TRIAGE LEVEL: {res['level']}** (Confidence: {res['confidence_score']}%)")
            else:
                st.success(f"🟢 **TRIAGE LEVEL: {res['level']}** (Confidence: {res['confidence_score']}%)")
                
            st.markdown(f"**Clinical Guidance:** {res['guidance']}")
            st.markdown(f"**Recommended First-Aid:** {res['first_aid']}")
            st.markdown(f"**Triage Action:** {res['triage']}")
            
            if st.button("🖨️ Print Clinical Summary Report"):
                st.toast("Clinical report compiled successfully!")
        else:
            st.markdown("No active symptom logs for today. Run an analysis to populate the clinical timeline.")
            st.info("🕒 *Previous Log:* Mild Stress (Resolved)")

elif selected_tab == "Journal & Mood History":
    st.subheader("📅 Weekly Emotional Tracking Timeline")
    st.line_chart([2, 3, 4, 3, 5, 2, 3]) # Sample mood trend chart
    st.markdown("Track your daily mood scores from 1 (Low) to 5 (High) to monitor patterns over time.")

elif selected_tab == "Crisis Support & Helplines":
    st.subheader("🚨 Immediate Crisis Helplines & Resources")
    st.error("""
    **If you are in immediate danger or experiencing thoughts of self-harm, please reach out for help right away:**
    * **National Crisis Helpline (US/Canada):** Call or text **988**
    * **Emergency Services:** Call **911** or your local emergency number
    * **International Resources:** Visit [findahelpline.com](https://findahelpline.com) to find confidential support in your country.
    """)
