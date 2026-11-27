"""
StudyMate AI Documentation Page
--------------------------------
Add this module to your existing Streamlit project as documentation.py.

Integration in app.py:
    from documentation import render_documentation

Add "Documentation" to your page navigation, then:
    elif page == "Documentation":
        render_documentation()

This is a documentation UI module. Code examples are educational snippets;
adapt names/paths if your local implementation differs.
"""

import streamlit as st


DOCS = [
    {
        "category": "Getting Started",
        "title": "Introduction",
        "description": "Understand what StudyMate AI does and how its modules work together.",
        "body": """
# StudyMate AI

StudyMate AI is an AI-powered student learning assistant built with Python,
Streamlit, Google Gemini and SQLite.

## Main capabilities

- AI Chat Assistant with tool calling
- Quiz generation and interactive quiz attempts
- Notes summarization
- Study planning
- Safe calculator
- Persistent conversations and feature history
- Quiz progress and attempt history

## Application flow

1. A student selects a feature in the Streamlit interface.
2. The application validates the input.
3. The AI agent or a dedicated Python tool processes the request.
4. The result is validated and displayed.
5. Relevant data is stored in SQLite for later use.

> The exact implementation may differ slightly between project versions.
  """,
        "code": ("text", "StudyMate AI\n├── app.py             # Streamlit user interface\n├── agent.py           # Gemini AI agent and tool orchestration\n├── tools.py           # Calculator, quiz, summarizer and planner tools\n├── db.py              # SQLite connection and database functions\n├── requirements.txt   # Python dependencies\n├── .env               # Local API key (never commit this file)\n└── studymate.db       # Local SQLite database"),
    },
    {
        "category": "Getting Started",
        "title": "Installation & Setup",
        "description": "Prepare Python, create a virtual environment and install dependencies.",
        "body": """
# Installation & Setup

## Requirements

- Windows, macOS or Linux
- Python 3.10 or newer (use the version tested by your project)
- A Google Gemini API key
- VS Code or another Python editor

## 1. Open the project folder

Open a terminal in the `studymate-ai` project directory.

## 2. Create a virtual environment

A virtual environment keeps project dependencies isolated.

## 3. Activate the environment

On Windows PowerShell, use the activation command shown below. In Git Bash,
use the corresponding `source` command.

## 4. Install dependencies

Install the packages listed in `requirements.txt`.

## 5. Configure the API key

Create a `.env` file in the project root. Do not upload or commit this file.
  """,
        "code": ("bash", "# Windows PowerShell\npy -m venv venv\n.\\venv\\Scripts\\Activate.ps1\n\n# Git Bash\nsource venv/Scripts/activate\n\n# Install dependencies\npython -m pip install -r requirements.txt"),
    },
    {
        "category": "Getting Started",
        "title": "Environment Variables",
        "description": "Configure Gemini securely without placing secrets in source code.",
        "body": """
# Environment Variables

Create `.env` in the project root:

- Add your Gemini API key as `GEMINI_API_KEY`.
- Keep `.env` in `.gitignore`.
- Never paste API keys into screenshots, public repositories or documentation.

Load variables with `python-dotenv`. The application should show a helpful
configuration error if the key is missing.
  """,
        "code": ("dotenv", "GEMINI_API_KEY=your_gemini_api_key_here"),
    },
    {
        "category": "Architecture",
        "title": "Project Structure",
        "description": "Learn the responsibilities of the main Python files.",
        "body": """
# Project Structure

| File | Responsibility |
|---|---|
| `app.py` | Streamlit pages, forms, session state and UI rendering |
| `agent.py` | Gemini client, system instructions, tool calling and AI responses |
| `tools.py` | Validated Python functions used by the agent |
| `db.py` | SQLite connection, schema initialization and CRUD helpers |
| `requirements.txt` | Python package dependencies |
| `.env` | Local secrets; do not commit |
| `studymate.db` | Persistent SQLite database |

Keep UI code, AI orchestration, tools and database operations separated.
This makes the application easier to test and extend.
  """,
        "code": ("python", "# Example: importing the agent into the Streamlit UI\nfrom agent import agent\n\nresponse = agent.ask(user_message)\nst.write(response)"),
    },
    {
        "category": "Architecture",
        "title": "Application Flow",
        "description": "Follow a request from the user interface through the agent and database.",
        "body": """
# Application Flow

## AI chat request

1. The user enters a message in `app.py`.
2. The UI retrieves the current conversation context.
3. `agent.py` sends the request to Gemini.
4. Gemini may answer directly or request a registered tool.
5. The agent executes the tool and returns the result to Gemini.
6. The final response is shown in Streamlit.
7. User and assistant messages are saved through `db.py`.

## Feature request

Dedicated features such as quiz generation can call a specific agent method
or Python tool, validate its structured result, display it, and save a feature
history record.
  """,
        "code": ("text", "Student\n   ↓\nStreamlit UI (app.py)\n   ↓\nAgent / Feature Controller (agent.py)\n   ↓\nGemini API  ↔  Python Tools (tools.py)\n   ↓\nValidation\n   ↓\nSQLite Database (db.py)\n   ↓\nResult shown to student"),
    },
    {
        "category": "AI Agent",
        "title": "Gemini Agent",
        "description": "Understand the AI client, system instructions and tool orchestration.",
        "body": """
# Gemini Agent

The agent is responsible for communicating with Gemini and coordinating
available Python tools.

Typical responsibilities:

- Load the API key from environment variables.
- Initialize the Gemini client.
- Define the assistant's system instructions.
- Register tool declarations.
- Process model responses and tool calls.
- Validate tool arguments and results.
- Handle temporary API errors and timeouts.

Keep the model name configurable in one place. Model availability and quotas
can change, so verify the model name in your Google AI Studio project.
  """,
        "code": ("python", "import os\nfrom dotenv import load_dotenv\nfrom google import genai\n\nload_dotenv()\napi_key = os.getenv(\"GEMINI_API_KEY\")\n\nif not api_key:\n    raise RuntimeError(\"GEMINI_API_KEY is not configured\")\n\nclient = genai.Client(api_key=api_key)"),
    },
    {
        "category": "AI Agent",
        "title": "Tool Calling",
        "description": "Learn why an agent uses tools instead of asking the language model to do everything.",
        "body": """
# Tool Calling

Tool calling allows the model to request a specific Python function. Your
application executes that function and returns its result.

Examples:

- Calculator tool: performs a validated calculation.
- Quiz tool: validates and structures multiple-choice questions.
- Notes summarizer: creates a structured summary.
- Study planner: produces a study schedule.

Important: model-generated arguments are untrusted input. Validate types,
required fields, lengths and allowed values before executing a tool.
  """,
        "code": ("python", "def example_tool(topic: str) -> dict:\n    if not isinstance(topic, str) or not topic.strip():\n        return {\"success\": False, \"error\": \"Topic is required.\"}\n\n    return {\n        \"success\": True,\n        \"topic\": topic.strip()\n    }"),
    },
    {
        "category": "Features",
        "title": "AI Chat Assistant",
        "description": "Understand chat messages, conversation context and persistence.",
        "body": """
# AI Chat Assistant

The chat interface lets students ask questions and receive AI explanations.

Core concepts:

- A conversation groups related messages.
- Each message stores a role and content.
- Conversation history can be loaded from SQLite.
- The agent can use tools when a request requires computation or structured work.

For long conversations, manage context deliberately. Do not send unlimited
history to the model on every request.
  """,
        "code": ("python", "# Conceptual message persistence example\nsave_message(\n    conversation_id=conversation_id,\n    role=\"user\",\n    content=user_message\n)\n\nanswer = agent.ask(user_message)\n\nsave_message(\n    conversation_id=conversation_id,\n    role=\"assistant\",\n    content=answer\n)"),
    },
    {
        "category": "Features",
        "title": "Quiz Generator",
        "description": "Generate, validate and display multiple-choice questions.",
        "body": """
# Quiz Generator

The quiz workflow typically includes:

1. Collect topic, question count, difficulty and language.
2. Ask the AI to return structured questions.
3. Validate every question and its four options.
4. Verify that the correct answer matches one of the options.
5. Save the generated quiz to feature history.
6. Display one question at a time.
7. Save answers and current question index.
8. Calculate and persist the final result.

## Validation matters

AI output can contain extra punctuation, missing fields or malformed options.
Normalize harmless formatting differences, but never accept an answer that
does not match an available option.
  """,
        "code": ("python", "def normalize_answer(value: str) -> str:\n    import re\n    value = re.sub(r\"[^\\w\\s]\", \"\", str(value))\n    return \" \".join(value.casefold().split())\n\n# Compare a generated answer against available options\nmatched = next(\n    (option for option in options\n     if normalize_answer(option) == normalize_answer(correct_answer)),\n    None\n)\n\nif matched is None:\n    raise ValueError(\"Correct answer does not match any option\")"),
    },
    {
        "category": "Features",
        "title": "Quiz Scoring & Attempts",
        "description": "Understand scoring, grades, history and duplicate-submission protection.",
        "body": """
# Quiz Scoring & Attempts

A completed attempt should record:

- Topic and total question count
- Correct, incorrect and unanswered counts
- Percentage and grade
- Attempt timestamp
- A unique attempt identifier

Use a database uniqueness constraint on the attempt identifier to prevent
the same quiz submission from being saved more than once. A hidden button or
session-state flag alone is not a complete duplicate-prevention strategy.

Persist submitted state so a page refresh does not reopen a completed attempt.
  """,
        "code": ("python", "percentage = (correct_answers / total_questions) * 100\n\nif percentage >= 90:\n    grade = \"A+\"\nelif percentage >= 80:\n    grade = \"A\"\nelif percentage >= 70:\n    grade = \"B\"\nelif percentage >= 60:\n    grade = \"C\"\nelif percentage >= 50:\n    grade = \"D\"\nelse:\n    grade = \"F\""),
    },
    {
        "category": "Features",
        "title": "Notes Summarizer",
        "description": "Summarize learning material into concise, structured notes.",
        "body": """
# Notes Summarizer

A notes summarizer can accept pasted text and produce:

- A short summary
- Key points
- Important definitions
- Main concepts
- Revision questions

For uploaded documents, validate file type and size, extract text safely,
and report when a document contains no extractable text. Scanned documents
may require OCR.
  """,
        "code": ("python", "# Example input validation for pasted notes\nif not isinstance(notes, str) or not notes.strip():\n    st.warning(\"Please enter your notes first.\")\nelse:\n    summary = agent.summarize_notes(notes)\n    st.markdown(summary)"),
    },
    {
        "category": "Features",
        "title": "Study Planner",
        "description": "Create structured study plans and track learning tasks.",
        "body": """
# Study Planner

A study plan can include:

- Subject and topic
- Task description
- Priority
- Planned date
- Estimated duration
- Completion status

Store tasks in the database if they must survive a refresh. A generated plan
should be treated as a suggestion that the student can review and edit.
  """,
        "code": ("python", "study_plan = {\n    \"subject\": \"Computer Networks\",\n    \"topic\": \"Data Link Layer\",\n    \"duration_minutes\": 45,\n    \"priority\": \"High\",\n    \"completed\": False\n}"),
    },
    {
        "category": "Database",
        "title": "SQLite Database",
        "description": "Understand database initialization, connections and persistent records.",
        "body": """
# SQLite Database

SQLite stores application data in a local database file.

The existing project uses tables for conversations, messages, feature history,
quiz progress and quiz attempts.

Good practices:

- Enable foreign-key enforcement on each connection.
- Use parameterized SQL queries.
- Use transactions for related writes.
- Add indexes for frequently filtered columns.
- Back up the database before schema changes.
- Use versioned migrations instead of deleting the database.

The actual schema in your local `db.py` is the source of truth.
  """,
        "code": ("python", "import sqlite3\nfrom pathlib import Path\n\nDB_PATH = Path(__file__).resolve().parent / \"studymate.db\"\n\ndef get_connection():\n    connection = sqlite3.connect(DB_PATH)\n    connection.row_factory = sqlite3.Row\n    connection.execute(\"PRAGMA foreign_keys = ON\")\n    return connection"),
    },
    {
        "category": "Database",
        "title": "Session State & Persistence",
        "description": "Learn the difference between temporary UI state and database persistence.",
        "body": """
# Session State & Persistence

Streamlit session state holds values during a user's active session. It is
useful for the current conversation ID, selected page, quiz index and answers.

SQLite is used for durable data that must remain after a refresh or a new
session, such as conversations, quiz progress and quiz attempts.

Do not rely on session state alone for important records. Save them to the
database at the appropriate points in the workflow.
  """,
        "code": ("python", "if \"quiz_index\" not in st.session_state:\n    st.session_state[\"quiz_index\"] = 0\n\nst.session_state[\"quiz_index\"] += 1"),
    },
    {
        "category": "Analytics & Export",
        "title": "Performance Analytics",
        "description": "Turn real quiz attempt records into useful student insights.",
        "body": """
# Performance Analytics

Analytics should be calculated from actual quiz attempts.

Useful metrics:

- Total attempts
- Average and best score
- Topic-wise average
- Correct and incorrect answer totals
- Score trend over time

Plotly can display interactive line, bar and donut charts in Streamlit.
Show a clear empty state when there are not enough records for a meaningful
chart. Do not invent sample records in the real dashboard.
  """,
        "code": ("python", "import plotly.express as px\nimport pandas as pd\n\n# attempts should come from your database query\nframe = pd.DataFrame(attempts)\nif not frame.empty:\n    chart = px.line(\n        frame,\n        x=\"created_at\",\n        y=\"percentage\",\n        color=\"topic\",\n        title=\"Quiz Performance Over Time\"\n    )\n    st.plotly_chart(chart, use_container_width=True)\nelse:\n    st.info(\"Complete a quiz to see your performance analytics.\")"),
    },
    {
        "category": "Analytics & Export",
        "title": "Download & Export",
        "description": "Offer downloadable quiz results and learning reports.",
        "body": """
# Download & Export

Streamlit's download button can provide files generated in memory.

Recommended formats:

- PDF for formatted reports
- CSV for spreadsheet analysis
- JSON for structured data exchange
- TXT for simple notes

For PDF generation, ReportLab is a suitable Python library. Use an appropriate
Unicode font when generating Bangla documents and test the resulting PDF.
  """,
        "code": ("python", "import json\nimport streamlit as st\n\nreport = {\n    \"topic\": \"Computer Networks\",\n    \"total_questions\": 10,\n    \"correct_answers\": 8,\n    \"percentage\": 80\n}\n\npayload = json.dumps(report, ensure_ascii=False, indent=2)\nst.download_button(\n    \"Download JSON\",\n    data=payload,\n    file_name=\"quiz-report.json\",\n    mime=\"application/json\"\n)"),
    },
    {
        "category": "Development",
        "title": "Testing & Troubleshooting",
        "description": "Run tests and diagnose common development problems.",
        "body": """
# Testing & Troubleshooting

## Run the application

Run Streamlit from the project root with the virtual environment activated.

## Common problems

- `GEMINI_API_KEY` missing: check `.env` and restart the app.
- Module not found: activate the correct virtual environment and install requirements.
- SQLite table missing: verify that `init_db()` runs before database queries.
- Quiz answer mismatch: inspect the raw AI output and answer normalization.
- Duplicate quiz attempts: use a unique attempt ID and database constraint.
- Git command not found: repair Git for Windows installation and PATH.

When debugging, read the complete traceback and fix the first relevant error.
  """,
        "code": ("bash", "# Activate your virtual environment, then:\npython -m pip install -r requirements.txt\nstreamlit run app.py\n\n# Optional test command if pytest tests exist\npython -m pytest -q"),
    },
    {
        "category": "Development",
        "title": "Git & Safe Project Backup",
        "description": "Track code changes without publishing secrets or private database data.",
        "body": """
# Git & Safe Project Backup

Before a major upgrade:

1. Commit or copy the working source code.
2. Keep `.env`, virtual environments and local databases out of public Git.
3. Review `.gitignore`.
4. Create a database backup before migrations.
5. Test changes on a copy of the database.

Never upload API keys or private student records to a public repository.
  """,
        "code": ("gitignore", "venv/\n.env\n__pycache__/\n*.pyc\n.streamlit/secrets.toml\nstudymate.db\n"),
    },

    {
        "category": "Project Information",
        "title": "Developer Team",
        "description": "Meet the developers behind StudyMate AI.",
        "body": """
# Developer Team

StudyMate AI is developed and maintained by the following team members.

## Project Developers

- **Md Abdul Shuqqre Hridoy (240312023)**
- **Md Jahid Hossine (240312017)**

This section recognizes the developers who contributed to the StudyMate AI project.
  """,
        "code": ("text", "StudyMate AI\nProject Developers\n\n1. Md Abdul Shuqqre Hridoy (240312023)\n2. Md Jahid Hossine (240312017)"),
    },
]


def _inject_docs_css(theme: str) -> None:
    if theme == "Dark":
        bg, panel, text, muted, border, accent = "#0b1220", "#111c2e", "#e5edf8", "#9aabc2", "#26364d", "#65a9ff"
    else:
        bg, panel, text, muted, border, accent = "#ffffff", "#f5f7fb", "#172033", "#637083", "#dce3ed", "#1769d2"

    st.markdown(
        f"""
        <style>
        .docs-shell {{
            background: {bg};
            color: {text};
            border: 1px solid {border};
            border-radius: 16px;
            padding: 1.1rem 1.25rem;
            margin-bottom: 1rem;
        }}
        .docs-kicker {{
            color: {accent};
            font-size: .78rem;
            font-weight: 700;
            letter-spacing: .11em;
            text-transform: uppercase;
        }}
        .docs-muted {{ color: {muted}; }}
        .docs-card {{
            background: {panel};
            border: 1px solid {border};
            border-radius: 12px;
            padding: .9rem 1rem;
            margin: .5rem 0;
        }}
        .docs-card a {{ color: {accent}; }}
        div[data-testid="stCode"] {{
            border: 1px solid {border};
            border-radius: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_documentation() -> None:
    """Render the StudyMate AI documentation page inside Streamlit."""

    st.session_state.setdefault("docs_theme", "Dark")
    st.session_state.setdefault("docs_page", "Introduction")

    _inject_docs_css(st.session_state["docs_theme"])

    st.markdown(
        """
        <div class="docs-shell">
          <div class="docs-kicker">STUDYMATE AI / DEVELOPER DOCUMENTATION</div>
          <h1 style="margin:.35rem 0 .25rem 0;">StudyMate AI Docs</h1>
          <p class="docs-muted" style="margin:0;">
            Setup, architecture, features, database, AI tools and development guide.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns([4, 1])
    with top_left:
        search = st.text_input(
            "Search documentation",
            placeholder="Search setup, quiz, database, Gemini, export...",
            label_visibility="collapsed",
            key="docs_search",
        )
    with top_right:
        theme = st.selectbox(
            "Theme",
            ["Dark", "Light"],
            index=0 if st.session_state["docs_theme"] == "Dark" else 1,
            label_visibility="collapsed",
            key="docs_theme_select",
        )
        if theme != st.session_state["docs_theme"]:
            st.session_state["docs_theme"] = theme
            st.rerun()

    categories = {}
    for item in DOCS:
        categories.setdefault(item["category"], []).append(item)

    if search.strip():
        term = search.casefold().strip()
        visible = [
            item for item in DOCS
            if term in item["title"].casefold()
            or term in item["description"].casefold()
            or term in item["body"].casefold()
            or term in item["category"].casefold()
            or term in item["code"][1].casefold()
        ]
    else:
        visible = DOCS

    if not visible:
        st.warning("No documentation pages match your search.")
        return

    visible_titles = [item["title"] for item in visible]
    current_title = st.session_state.get("docs_page", "Introduction")
    if current_title not in visible_titles:
        current_title = visible_titles[0]
        st.session_state["docs_page"] = current_title

    nav_col, content_col = st.columns([1.05, 3.2], gap="large")

    with nav_col:
        st.markdown("#### Contents")
        for category, items in categories.items():
            matching = [item for item in items if item in visible]
            if not matching:
                continue
            with st.expander(category, expanded=True):
                for item in matching:
                    if st.button(
                        item["title"],
                        key=f"docs_nav_{item['title']}",
                        use_container_width=True,
                        type="primary" if item["title"] == current_title else "secondary",
                    ):
                        st.session_state["docs_page"] = item["title"]
                        st.rerun()

    selected = next(
        (item for item in visible if item["title"] == current_title),
        visible[0],
    )

    with content_col:
        st.markdown(f"<div class='docs-kicker'>{selected['category']}</div>", unsafe_allow_html=True)
        st.title(selected["title"])
        st.caption(selected["description"])
        st.markdown("---")
        st.markdown(selected["body"])

        language, source = selected["code"]
        st.markdown("### Code example")
        st.caption("Use the copy icon in the code block to copy this example.")
        st.code(source, language=language, line_numbers=True)

        st.markdown("---")
        index = visible_titles.index(selected["title"])
        previous_item = visible[index - 1] if index > 0 else None
        next_item = visible[index + 1] if index < len(visible_titles) - 1 else None
        prev_col, next_col = st.columns(2)
        with prev_col:
            if previous_item and st.button(
                f"← {previous_item['title']}",
                use_container_width=True,
            ):
                st.session_state["docs_page"] = previous_item["title"]
                st.rerun()
        with next_col:
            if next_item and st.button(
                f"{next_item['title']} →",
                use_container_width=True,
            ):
                st.session_state["docs_page"] = next_item["title"]
                st.rerun()

        st.caption("StudyMate AI documentation · Keep examples aligned with your current source code.")
