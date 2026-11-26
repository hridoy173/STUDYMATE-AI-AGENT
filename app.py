
import streamlit as st
from agent import agent

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="StudyMate AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #4F46E5;
        text-align: center;
    }

    .subtitle {
        text-align: center;
        color: #888888;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .feature-card {
        padding: 18px;
        border-radius: 14px;
        background: rgba(79, 70, 229, 0.08);
        border: 1px solid rgba(79, 70, 229, 0.15);
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("🎓 StudyMate AI")

    st.write(
        "Your intelligent AI-powered student assistant."
    )

    st.divider()

    st.subheader("🛠️ Available Tools")

    st.markdown("""
    - 🤖 AI Study Assistant
    - 📝 Notes Summarizer
    - 🧠 Quiz Generator
    - 📅 Study Planner
    - 🧮 Calculator
    """)

    st.divider()

    st.subheader("⚙️ Chat Settings")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Developed with Python, Gemini AI & Streamlit")

# -----------------------------
# Main Header
# -----------------------------
st.markdown(
    '<div class="main-title">🎓 StudyMate AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your Personal AI Learning Assistant'
    '</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Welcome Section
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:

    st.markdown("## 👋 Welcome to StudyMate AI!")

    st.write(
        "I can help you study, understand complex topics, "
        "generate quizzes, summarize notes, and create study plans."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 Learn</h3>
            <p>Understand academic topics in simple language.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 Practice</h3>
            <p>Generate MCQ quizzes and test your knowledge.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📅 Plan</h3>
            <p>Create structured study schedules.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🚀 Try these prompts")

    st.markdown("""
    - Explain the OSI Model in English and Bangla.
    - Generate 5 MCQ about Computer Networks.
    - Summarize my study notes.
    - Create a 7-day study plan for Python.
    - Calculate 25% of 8500.
    """)

# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input(
    "Ask StudyMate anything about your studies..."
)

if prompt:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("StudyMate AI is thinking..."):

            try:
                # response = agent.ask(prompt)
                # Build conversation context from previous messages
                history = st.session_state.messages[:-1]

                conversation_context = ""

                for message in history:
                    role = "Student" if message["role"] == "user" else "StudyMate AI"

                    conversation_context += (
                        f"\n{role}: {message['content']}\n"
                    )

                # Add the current question
                contextual_prompt = f"""
                You are StudyMate AI, an intelligent student assistant.

                Use the conversation history to understand follow-up questions.
                Answer the latest question based on the context when relevant.

                Previous conversation:
                {conversation_context}

                Current question:
                {prompt}
                """

                response = agent.ask(contextual_prompt)


                st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:

                error_message = f"An error occurred: {e}"

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
