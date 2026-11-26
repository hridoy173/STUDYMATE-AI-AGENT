
import streamlit as st

from db import (
    init_db,
    create_conversation,
    get_conversations,
    get_messages,
    save_message,
    update_conversation_title,
    delete_conversation
)
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



# =====================================
# DATABASE & SESSION INITIALIZATION
# =====================================

init_db()


# Initialize conversation ID
if "conversation_id" not in st.session_state:

    conversations = get_conversations()

    if conversations:
        st.session_state["conversation_id"] = conversations[0]["id"]
    else:
        st.session_state["conversation_id"] = create_conversation()


# Initialize messages independently
if "messages" not in st.session_state:

    st.session_state["messages"] = get_messages(
        st.session_state["conversation_id"]
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

    st.subheader("📚 Learning Workspace")

    selected_page = st.radio(
        "Choose a feature",
        [
            "AI Chat",
            "Quiz Generator",
            "Notes Summarizer",
            "Study Planner",
            "Calculator"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.subheader("💬 Conversations")

    # Create a new conversation
    if st.button("➕ New Chat", use_container_width=True):

        st.session_state["conversation_id"] = create_conversation()
        st.session_state.messages = []

        st.rerun()


    # Load previous conversations
    conversations = get_conversations()

    if conversations:

        conversation_ids = [
            conversation["id"]
            for conversation in conversations
        ]

        # current_id = st.session_state["conversation_id"]
        current_id = st.session_state["conversation_id"]

        selected_id = st.selectbox(
            "Previous Conversations",
            options=conversation_ids,
            index=(
                conversation_ids.index(current_id)
                if current_id in conversation_ids
                else 0
            ),
            format_func=lambda cid: next(
                (
                    item["title"]
                    for item in conversations
                    if item["id"] == cid
                ),
                "Untitled Chat"
            )
        )

    # Load selected conversation
    if selected_id != current_id:

        st.session_state["conversation_id"] = selected_id

        st.session_state.messages = get_messages(selected_id)

        st.rerun()


    # Delete current conversation
    if st.button("🗑️ Clear Current Chat", use_container_width=True):

        delete_conversation(st.session_state["conversation_id"])

        st.session_state["conversation_id"] = create_conversation()
        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption("Developed with Python,SQLlite,Gemini AI & Streamlit.Developed by the StudyMate AI Team (AS Hridoy & Md Jahid )")



# -----------------------------
# Main Header
# -----------------------------
st.markdown(
    '<div class="main-title">🎓 StudyMate AI Agent</div>',
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

    st.markdown("## 👋 Welcome to StudyMate AI Agent!")

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


# =====================================
# QUIZ GENERATOR PAGE
# =====================================

if selected_page == "Quiz Generator":

    st.title("🧠 Quiz Generator")

    st.write(
        "Generate AI-powered multiple-choice questions "
        "to test your knowledge."
    )

    with st.form("quiz_form"):

        topic = st.text_input(
            "Subject / Topic",
            placeholder="Example: Computer Networks"
        )

        number_of_questions = st.selectbox(
            "Number of Questions",
            [5, 10, 15, 20]
        )

        difficulty = st.selectbox(
            "Difficulty Level",
            ["Easy", "Medium", "Hard"]
        )

        language = st.selectbox(
            "Language",
            ["English", "Bangla", "English and Bangla"]
        )

        submitted = st.form_submit_button(
            "🚀 Generate Quiz",
            use_container_width=True
        )

    if submitted:

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            quiz_prompt = f"""
            Generate exactly {number_of_questions} MCQ questions
            about {topic}.

            Difficulty: {difficulty}
            Language: {language}

            Include:
            - Four options per question
            - Correct answer
            - Explanation for every answer

            Use the quiz_generator tool.
            """

            with st.spinner("Generating your quiz..."):

                try:

                    result = agent.ask(quiz_prompt)

                    st.markdown("### Your Quiz")
                    st.markdown(result)

                except Exception as e:

                    st.error(f"Quiz generation failed: {e}")

    st.stop()


# ==============================
# NOTES SUMMARIZER PAGE
# ==============================

if selected_page == "Notes Summarizer":

    st.title("📝 Notes Summarizer")
    st.write(
        "Paste your study notes and let AI turn them into "
        "easy-to-understand summaries."
    )

    with st.form("notes_summarizer_form"):

        notes = st.text_area(
            "Your Study Notes",
            placeholder="Paste your lecture notes, textbook content, or study materials here...",
            height=300
        )

        col1, col2 = st.columns(2)

        with col1:
            summary_length = st.selectbox(
                "Summary Length",
                ["Short", "Medium", "Detailed"]
            )

        with col2:
            summary_language = st.selectbox(
                "Summary Language",
                ["English", "Bangla", "English and Bangla"]
            )

        include_key_points = st.checkbox(
            "Include important key points",
            value=True
        )

        submitted = st.form_submit_button(
            "✨ Summarize Notes",
            use_container_width=True
        )

    if submitted:

        if not notes.strip():
            st.warning("Please paste your study notes first.")

        elif len(notes.strip()) < 30:
            st.warning(
                "Please provide at least 30 characters of notes "
                "for a meaningful summary."
            )

        else:

            summarizer_prompt = f"""
            You are StudyMate AI, an intelligent student assistant.

            Summarize the following study notes.

            Summary Length: {summary_length}
            Language: {summary_language}
            Include Key Points: {include_key_points}

            Instructions:
            - Use the notes_summarizer tool.
            - Preserve the original meaning of the notes.
            - Use simple, student-friendly language.
            - Do not invent information that is not present in the notes.
            - Organize the summary with clear headings.
            - If key points are requested, include important points
              in bullet lists.
            - If the language is Bangla, explain technical terms
              in English where necessary.
            - If English and Bangla are requested, provide both.

            Study Notes:
            {notes}
            """

            with st.spinner("AI is analyzing your notes..."):

                try:

                    result = agent.ask(summarizer_prompt)

                    st.markdown("---")
                    st.subheader("📖 Summary Result")

                    st.markdown(result)

                except Exception as e:

                    st.error("Failed to summarize notes.")

                    st.info(
                        "Please try again in a few moments."
                    )

    st.stop()


# ==============================
# STUDY PLANNER PAGE
# ==============================

if selected_page == "Study Planner":

    st.title("📅 Study Planner")
    st.write(
        "Create a personalized study schedule with StudyMate AI."
    )

    with st.form("study_planner_form"):

        subject = st.text_input(
            "Subject",
            placeholder="Example: Computer Networks"
        )

        topics = st.text_area(
            "Topics to Study",
            placeholder="Enter topics separated by commas or new lines...",
            height=200
        )

        col1, col2 = st.columns(2)

        with col1:
            days = st.number_input(
                "Study Duration (Days)",
                min_value=1,
                max_value=365,
                value=7
            )

        with col2:
            hours_per_day = st.number_input(
                "Study Hours Per Day",
                min_value=1,
                max_value=24,
                value=3
            )

        language = st.selectbox(
            "Plan Language",
            ["English", "Bangla", "English and Bangla"]
        )

        submitted = st.form_submit_button(
            "🚀 Generate Study Plan",
            use_container_width=True
        )

    if submitted:

        if not subject.strip():
            st.warning("Please enter a subject.")

        elif not topics.strip():
            st.warning("Please enter the topics you want to study.")

        else:

            planner_prompt = f"""
            You are StudyMate AI, an intelligent academic study planner.

            Create a personalized study schedule.

            Subject: {subject}
            Topics: {topics}
            Total Days: {days}
            Study Hours Per Day: {hours_per_day}
            Language: {language}

            Instructions:
            - Use the study_planner tool.
            - Create a day-by-day study schedule.
            - Distribute topics evenly across the available days.
            - Respect the daily study time.
            - Include short breaks where appropriate.
            - Include revision sessions.
            - Include practice questions or exercises.
            - Include a final revision session if possible.
            - Do not omit any topic provided by the student.
            - Make the plan realistic and easy to follow.
            - Use a clear table or structured format.
            - Explain in the selected language.
            """

            with st.spinner("Creating your personalized study plan..."):

                try:

                    result = agent.ask(planner_prompt)

                    st.markdown("---")
                    st.subheader("📚 Your Study Plan")

                    st.markdown(result)

                except Exception:

                    st.error("Failed to generate study plan.")

                    st.info(
                        "Please try again in a few moments."
                    )

    st.stop()


# ==============================
# CALCULATOR PAGE
# ==============================

if selected_page == "Calculator":

    st.title("🧮 Calculator")
    st.write("Perform calculations instantly without using AI.")

    with st.form("calculator_form"):

        col1, col2 = st.columns(2)

        with col1:
            num1 = st.number_input(
                "First Number",
                value=0.0,
                format="%g"
            )

        with col2:
            num2 = st.number_input(
                "Second Number",
                value=0.0,
                format="%g"
            )

        operation = st.selectbox(
            "Select Operation",
            [
                "Addition (+)",
                "Subtraction (-)",
                "Multiplication (×)",
                "Division (÷)",
                "Modulus (%)",
                "Power (^)",
                "Percentage (%)"
            ]
        )

        calculate_button = st.form_submit_button(
            "🧮 Calculate",
            use_container_width=True
        )

    if calculate_button:

        try:

            if operation == "Addition (+)":
                result = num1 + num2

            elif operation == "Subtraction (-)":
                result = num1 - num2

            elif operation == "Multiplication (×)":
                result = num1 * num2

            elif operation == "Division (÷)":

                if num2 == 0:
                    st.error("Cannot divide by zero.")
                    st.stop()

                result = num1 / num2

            elif operation == "Modulus (%)":

                if num2 == 0:
                    st.error("Cannot calculate modulus with zero.")
                    st.stop()

                result = num1 % num2

            elif operation == "Power (^)":
                result = num1 ** num2

            elif operation == "Percentage (%)":
                result = (num1 * num2) / 100

            st.markdown("---")

            st.subheader("📊 Calculation Result")

            st.success(f"Result: {result}")

            if operation == "Percentage (%)":
                st.caption(
                    f"{num2}% of {num1} = {result}"
                )

        except Exception as e:

            st.error(f"Calculation error: {e}")

    st.info(
        "💡 This calculator works locally and does not require a Gemini API request."
    )

    st.stop()

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

    # Save user message in session and database
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    save_message(
        st.session_state["conversation_id"],
        "user",
        prompt
    )

    # Set conversation title using the first message
    if len(st.session_state.messages) == 1:

        update_conversation_title(
            st.session_state["conversation_id"],
            prompt
        )

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

                # Save AI response in session and database

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

                save_message(
                    st.session_state["conversation_id"],
                    "assistant",
                    response
                )

            except Exception as e:

                error_message = f"An error occurred: {e}"

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
