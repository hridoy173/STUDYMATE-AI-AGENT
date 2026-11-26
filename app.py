
import streamlit as st

from db import (
    init_db,
    create_conversation,
    get_conversations,
    get_messages,
    save_message,
    update_conversation_title,
    delete_conversation,
    save_feature_history,
    get_feature_history,
    save_quiz_progress,
    get_quiz_progress,
    delete_quiz_progress,
    save_quiz_attempt,
    get_quiz_attempts,
)

from agent import agent



## Display Feature History

def display_feature_history(feature_name):

    history = get_feature_history(
        st.session_state["conversation_id"],
        feature_name
    )

    st.markdown("---")
    st.subheader(f"📚 Previous {feature_name} History")

    if not history:
        st.info("No previous results found.")
        return

    for item in history:

        with st.expander(
            f"{feature_name} — {item['created_at']}"
        ):

            st.markdown("**Input Details**")
            st.json(item["input_data"])

            st.markdown("**Generated Result**")
            st.markdown(item["output_data"])


def display_quiz_attempt_history():
    st.subheader("📊 Quiz Performance History")

    conversation_id = st.session_state["conversation_id"]

    attempts = get_quiz_attempts(conversation_id)

    if not attempts:
        st.info("No quiz attempts found yet.")
        return

    for attempt in attempts:
        with st.expander(
            f"{attempt['topic']} | {attempt['percentage']:.1f}% | Grade {attempt['grade']}"
        ):
            col1, col2, col3 = st.columns(3)

            col1.metric("Correct", attempt["correct_answers"])
            col2.metric("Incorrect", attempt["wrong_answers"])
            col3.metric("Unanswered", attempt["unanswered"])

            st.write(f"**Total Questions:** {attempt['total_questions']}")
            st.write(f"**Score:** {attempt['percentage']:.2f}%")
            st.write(f"**Grade:** {attempt['grade']}")
            st.caption(f"Attempt ID: {attempt['id']}")
            st.caption(f"Date: {attempt['created_at']}")


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

    st.title("🎓 StudyMate Agent")

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

    st.caption("Developed with Python,SQLlite,Gemini AI & Streamlit.Developed by the StudyMate AI Agent Team (AS Hridoy & Md Jahid )")



# -----------------------------
# Main Header
# -----------------------------
st.markdown(
    '<div class="main-title">🎓 StudyMate Agent</div>',
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

    import json

    st.title("🧠 Interactive Quiz Generator")

    st.write(
        "Generate MCQs, answer questions, submit your quiz "
        "and check your score."
    )

    # Load quiz progress from database
    if st.session_state.get("quiz_conversation_id") != st.session_state["conversation_id"]:

        conversation_id = st.session_state["conversation_id"]

        st.session_state["quiz_conversation_id"] = conversation_id

        progress = get_quiz_progress(conversation_id)

        if progress:

            st.session_state["quiz_data"] = progress["quiz_data"]
            st.session_state["quiz_answers"] = progress["answers"]
            st.session_state["quiz_index"] = progress["current_index"]
            st.session_state["quiz_submitted"] = progress["is_submitted"]

            # Restore selected radio answers
            for index, answer in progress["answers"].items():
                st.session_state[f"quiz_answer_{index}"] = answer

        else:

            st.session_state.pop("quiz_data", None)
            st.session_state.pop("quiz_answers", None)
            st.session_state.pop("quiz_index", None)
            st.session_state.pop("quiz_submitted", None)


    # Quiz generation form
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

    # Generate structured quiz
    if submitted:

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            with st.spinner("Generating your interactive quiz..."):

                result = agent.generate_quiz(
                    topic=topic,
                    number_of_questions=number_of_questions,
                    difficulty=difficulty,
                    language=language
                )

            if result["success"]:

                st.session_state["quiz_data"] = result
                st.session_state["quiz_answers"] = {}
                st.session_state["quiz_index"] = 0
                st.session_state["quiz_submitted"] = False

                save_quiz_progress(
                    st.session_state["conversation_id"],
                    st.session_state["quiz_data"],
                    st.session_state["quiz_answers"],
                    st.session_state["quiz_index"],
                    False
                )

                # Clear previous radio selections
                for i in range(len(result["questions"])):
                    st.session_state.pop(f"quiz_answer_{i}", None)

                formatted_result = ""

                for index, question in enumerate(result["questions"], start=1):

                    formatted_result += f"""
                ### Question {index}

                **{question['question']}**

                """

                    for option_index, option in enumerate(question["options"], start=1):
                        formatted_result += f"{option_index}. {option}\n"

                    formatted_result += f"""
                **Correct Answer:** {question['correct_answer']}

                **Explanation:** {question['explanation']}

                ---
                """

                save_feature_history(
                    st.session_state["conversation_id"],
                    "Quiz Generator",
                    {
                        "topic": topic,
                        "questions": number_of_questions,
                        "difficulty": difficulty,
                        "language": language
                    },
                    formatted_result
                )

                st.success("Quiz generated successfully!")

            else:

                st.error(
                    f"Quiz generation failed: {result['error']}"
                )

    # Display active quiz
    if "quiz_data" in st.session_state:

        quiz = st.session_state["quiz_data"]
        questions = quiz["questions"]
        total_questions = len(questions)

        st.divider()

        st.subheader(f"📚 {quiz['topic']}")

        st.caption(
            f"Total Questions: {total_questions}"
        )

        # Show quiz result after submission
        if st.session_state.get("quiz_submitted", False):

            answers = st.session_state["quiz_answers"]

            correct_count = sum(
                1
                for i, question in enumerate(questions)
                if answers.get(i) == question["correct_answer"]
            )

            wrong_count = total_questions - correct_count
            percentage = (correct_count / total_questions) * 100

            if percentage >= 90:
                grade = "A+"
            elif percentage >= 80:
                grade = "A"
            elif percentage >= 70:
                grade = "B"
            elif percentage >= 60:
                grade = "C"
            elif percentage >= 50:
                grade = "D"
            else:
                grade = "F"

            # Save Result to Database
            save_quiz_attempt(
                conversation_id=st.session_state["conversation_id"],
                topic= quiz["topic"],
                total_questions=total_questions,
                correct_answers=correct_count,
                wrong_answers=wrong_count,
                unanswered=total_questions - len(answers),
                percentage=percentage,
                grade=grade
            )

            st.divider()

            st.success("Quiz Submitted Successfully!")

            st.subheader("🏆 Your Quiz Result")

            col1, col2, col3 , col4 = st.columns(4)

            col1.metric(
                "Correct Answers",
                correct_count
            )

            col2.metric(
                "Wrong / Unanswered",
                wrong_count
            )

            col3.metric(
                "Score",
                f"{percentage:.1f}%"
            )

            col4.metric(
                "Grade","{grade}%"
            )

            st.progress(percentage / 100)

            st.markdown("### 📝 Answer Review")

            for i, question in enumerate(questions):

                student_answer = answers.get(i)

                is_correct = (
                    student_answer == question["correct_answer"]
                )

                with st.expander(
                    f"Question {i + 1} — "
                    f"{'✅ Correct' if is_correct else '❌ Incorrect'}"
                ):

                    st.write(question["question"])

                    st.write(
                        f"**Your Answer:** "
                        f"{student_answer or 'Not answered'}"
                    )

                    st.write(
                        f"**Correct Answer:** "
                        f"{question['correct_answer']}"
                    )

                    st.info(
                        f"Explanation: {question['explanation']}"
                    )

            if st.button(
                "🔄 Try Another Quiz",
                use_container_width=True
            ):

                delete_quiz_progress(st.session_state["conversation_id"])

                st.session_state.pop("quiz_data", None)
                st.session_state.pop("quiz_answers", None)
                st.session_state.pop("quiz_index", None)
                st.session_state.pop("quiz_submitted", None)

                for i in range(total_questions):
                    st.session_state.pop(f"quiz_answer_{i}", None)

                st.rerun()

        else:

            current_index = st.session_state["quiz_index"]
            question = questions[current_index]

            # Progress
            st.progress(
                (current_index + 1) / total_questions
            )

            st.caption(
                f"Question {current_index + 1} of {total_questions}"
            )

            st.subheader(question["question"])

            # Answer selection
            selected_answer = st.radio(
                "Select your answer:",
                options=question["options"],
                index=None,
                key=f"quiz_answer_{current_index}"
            )

            if selected_answer is not None:

                st.session_state["quiz_answers"][current_index] = selected_answer

                save_quiz_progress(
                    st.session_state["conversation_id"],
                    st.session_state["quiz_data"],
                    st.session_state["quiz_answers"],
                    current_index,
                    False
                )

            answered_count = len(
                st.session_state["quiz_answers"]
            )

            st.caption(
                f"Answered: {answered_count}/{total_questions}"
            )

            st.divider()

            # Navigation buttons
            col1, col2, col3 = st.columns(3)

            with col1:

                if current_index > 0:

                    if st.button("⬅️ Previous", use_container_width=True):

                        st.session_state["quiz_index"] -= 1

                        save_quiz_progress(
                            st.session_state["conversation_id"],
                            st.session_state["quiz_data"],
                            st.session_state["quiz_answers"],
                            st.session_state["quiz_index"],
                            False
                        )

                        st.rerun()

            with col2:

                if current_index < total_questions - 1:

                   if st.button("Next ➡️", use_container_width=True):

                        st.session_state["quiz_index"] += 1

                        save_quiz_progress(
                            st.session_state["conversation_id"],
                            st.session_state["quiz_data"],
                            st.session_state["quiz_answers"],
                            st.session_state["quiz_index"],
                            False
                        )

                        st.rerun()

            with col3:

                if st.button("📤 Submit Quiz", use_container_width=True):

                    st.session_state["quiz_submitted"] = True

                    save_quiz_progress(
                        st.session_state["conversation_id"],
                        st.session_state["quiz_data"],
                        st.session_state["quiz_answers"],
                        st.session_state["quiz_index"],
                        True
                    )

                    st.rerun()

    display_feature_history("Quiz Generator")
    display_quiz_attempt_history()

    st.stop()


# =====================================
# QUIZ GENERATOR PAGE
# =====================================

# if selected_page == "Quiz Generator":

#     st.title("🧠 Quiz Generator")

#     st.write(
#         "Generate AI-powered multiple-choice questions "
#         "to test your knowledge."
#     )

#     with st.form("quiz_form"):

#         topic = st.text_input(
#             "Subject / Topic",
#             placeholder="Example: Computer Networks"
#         )

#         number_of_questions = st.selectbox(
#             "Number of Questions",
#             [5, 10, 15, 20]
#         )

#         difficulty = st.selectbox(
#             "Difficulty Level",
#             ["Easy", "Medium", "Hard"]
#         )

#         language = st.selectbox(
#             "Language",
#             ["English", "Bangla", "English and Bangla"]
#         )

#         submitted = st.form_submit_button(
#             "🚀 Generate Quiz",
#             use_container_width=True
#         )

#     if submitted:

#         if not topic.strip():

#             st.warning("Please enter a topic.")

#         else:

#             quiz_prompt = f"""
#             Generate exactly {number_of_questions} MCQ questions
#             about {topic}.

#             Difficulty: {difficulty}
#             Language: {language}

#             Include:
#             - Four options per question
#             - Correct answer
#             - Explanation for every answer

#             Use the quiz_generator tool.
#             """

#             with st.spinner("Generating your quiz..."):

#                 try:

#                     result = agent.ask(quiz_prompt)

#                     save_feature_history(
#                         st.session_state["conversation_id"],
#                         "Quiz Generator",
#                         {
#                             "topic": topic,
#                             "questions": number_of_questions,
#                             "difficulty": difficulty,
#                             "language": language
#                         },
#                         result
#                     )

#                     st.success("Quiz generated and saved successfully!")

#                 except Exception as e:

#                     st.error(f"Quiz generation failed: {e}")

#     display_feature_history("Quiz Generator")

#     st.stop()


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

                    save_feature_history(
                        st.session_state["conversation_id"],
                        "Notes Summarizer",
                        {
                            "notes": notes,
                            "summary_length": summary_length,
                            "language": summary_language,
                            "include_key_points": include_key_points
                        },
                        result
                    )

                    st.success("Summary generated and saved successfully!")

                except Exception as e:

                    st.error("Failed to summarize notes.")

                    st.info(
                        "Please try again in a few moments."
                    )

    display_feature_history("Notes Summarizer")

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

                    save_feature_history(
                        st.session_state["conversation_id"],
                        "Study Planner",
                        {
                            "subject": subject,
                            "topics": topics,
                            "days": days,
                            "hours_per_day": hours_per_day,
                            "language": language
                        },
                        result
                    )

                    st.success("Study plan generated and saved successfully!")

                except Exception:

                    st.error("Failed to generate study plan.")

                    st.info(
                        "Please try again in a few moments."
                    )
                    
    display_feature_history("Study Planner")

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

            save_feature_history(
                    st.session_state["conversation_id"],
                    "Calculator",
                    {
                        "first_number": num1,
                        "second_number": num2,
                        "operation": operation
                    },
                    str(result)
                )

            st.markdown("---")

            st.subheader("📊 Calculation Result")

            st.success(f"Result: {result}")

            if operation == "Percentage (%)":
                st.caption(
                    f"{num2}% of {num1} = {result}"
                )

        except Exception as e:

            st.error(f"Calculation error: {e}")

    st.info("💡 This calculator works locally and does not require a Gemini API request.")

    display_feature_history("Calculator")

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

        with st.spinner("StudyMate AI Agent is thinking..."):

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
