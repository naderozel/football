import streamlit as st
from groq import Groq

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Football AI",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# COMPACT CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    padding: 0.25rem 1rem !important;
    max-width: 1400px !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.1rem !important;
}

.football-title {
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    color: #0b5d1e;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1;
}

.football-subtitle {
    text-align: center;
    font-size: 13px;
    color: #666;
    margin: 2px 0 4px 0 !important;
    padding: 0 !important;
}

.category-card {
    background: white;
    padding: 6px 9px !important;
    margin: 0 !important;
    border-radius: 7px;
    border: 1px solid #ddd;
    line-height: 1.1;
}

.category-card h3 {
    font-size: 15px;
    margin: 0 !important;
    padding: 0 !important;
}

.category-card p {
    font-size: 11px;
    margin: 2px 0 0 0 !important;
    padding: 0 !important;
    line-height: 1.15;
}

div[data-testid="stAlert"] {
    padding: 4px 8px !important;
    margin: 2px 0 !important;
}

div[data-testid="stChatMessage"] {
    padding: 0 !important;
    margin: 0 !important;
}

div[data-testid="stChatMessageContent"] {
    padding: 0 !important;
    margin: 0 !important;
}

.stButton {
    margin: 0 !important;
    padding: 0 !important;
}

.stButton > button {
    min-height: 25px !important;
    height: 25px !important;
    padding: 0 5px !important;
    margin: 0 !important;
    border-radius: 5px;
    font-size: 11px;
}

section[data-testid="stSidebar"] .block-container {
    padding: 0.25rem 0.5rem !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    margin: 1px 0 !important;
    padding: 0 !important;
}

section[data-testid="stSidebar"] p {
    margin: 1px 0 !important;
    padding: 0 !important;
    font-size: 12px;
}

section[data-testid="stSidebar"] hr {
    margin: 3px 0 !important;
}

div[data-testid="stMetric"] {
    padding: 0 !important;
    margin: 0 !important;
}

div[data-testid="stMetricLabel"] {
    font-size: 10px !important;
}

div[data-testid="stMetricValue"] {
    font-size: 18px !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# GROQ CLIENT
# ============================================================

try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except Exception:
    client = None

# ============================================================
# FIND AVAILABLE GROQ MODEL
# ============================================================

def get_available_model(client):

    # Preferred models, in order
    preferred_models = [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b"
    ]

    try:
        available_models = client.models.list()

        model_ids = [
            model.id
            for model in available_models.data
        ]

        # First try preferred models
        for model in preferred_models:
            if model in model_ids:
                return model

        # Otherwise find a usable chat model
        for model_id in model_ids:

            model_name = model_id.lower()

            if (
                "llama" in model_name
                or "gpt" in model_name
                or "qwen" in model_name
                or "mixtral" in model_name
            ):
                return model_id

        return None

    except Exception:
        return None


if client is not None:

    if "groq_model" not in st.session_state:

        st.session_state.groq_model = get_available_model(
            client
        )

# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are Football AI, a friendly and knowledgeable football
chatbot.

Talk primarily about association football (soccer).

You can discuss:

- Football rules
- Tactics
- Formations
- Clubs
- National teams
- Players
- Managers
- Football history
- Competitions
- Domestic leagues
- Champions League
- Europa League
- World Cup
- Women's football
- Youth football
- Transfers
- Statistics
- Famous matches
- Football terminology
- Training
- Positions
- Goalkeeping
- Defending
- Midfield
- Attacking
- Set pieces
- Penalties
- Offside
- VAR
- Football culture

Keep answers clear and useful.

Use short sections and bullet points when appropriate.

If the question is unrelated to football, politely explain
that you are a football-focused chatbot.

Do not claim to have live information.

For current scores, fixtures, standings, transfers, injuries,
or other changing information, explain that current information
needs to be checked using a reliable live source.

Be friendly and enthusiastic.
"""

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚽ Football AI")

    st.caption("Football chatbot")

    st.divider()

    st.subheader("📚 Topics")

    topics = [
        "⚽ Rules",
        "🏆 Competitions",
        "👤 Players",
        "🏟️ Clubs",
        "📋 Tactics",
        "🎯 Skills",
        "🌍 World Cup",
        "💰 Transfers",
        "📊 Statistics",
        "🧤 Goalkeeping"
    ]

    for topic in topics:
        st.write(topic)

    st.divider()

    st.subheader("💬 Examples")

    examples = [
        "What is offside?",
        "Explain 4-3-3.",
        "What does a DM do?",
        "How does VAR work?",
        "Football positions?",
        "Explain Champions League.",
        "What makes a good striker?",
        "What is a false nine?"
    ]

    for i, question in enumerate(examples):

        if st.button(
            question,
            key=f"example_{i}"
        ):

            st.session_state.pending_question = question
            st.rerun()

    st.divider()

    st.metric(
        "Questions",
        st.session_state.total_questions
    )

    if st.button("🗑️ Clear"):

        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        st.session_state.total_questions = 0
        st.session_state.pending_question = None

        st.rerun()

    st.divider()

    if client is not None:

        if st.session_state.get("groq_model"):

            st.caption(
                f"🤖 {st.session_state.groq_model}"
            )

        else:

            st.caption(
                "⚠️ No compatible Groq model found"
            )

    st.caption("⚽ Streamlit + Groq")

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="football-title">⚽ Football AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="football-subtitle">'
    'Football questions • Tactics • Players • Clubs • Competitions'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# WELCOME
# ============================================================

if len(st.session_state.messages) == 1:

    st.info(
        "👋 Ask me anything about football!"
    )

    col1, col2, col3 = st.columns(
        3,
        gap="small"
    )

    with col1:

        st.markdown("""
        <div class="category-card">
        <h3>🏆 Competitions</h3>
        <p>World Cup • Champions League • Leagues</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="category-card">
        <h3>📋 Tactics</h3>
        <p>Formations • Pressing • Possession</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="category-card">
        <h3>👤 Players</h3>
        <p>Positions • Roles • Skills</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

# ============================================================
# SIDEBAR QUESTION
# ============================================================

pending_question = st.session_state.pending_question

if pending_question:
    st.session_state.pending_question = None

# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "⚽ Ask a football question..."
)

if pending_question:
    prompt = pending_question

# ============================================================
# PROCESS QUESTION
# ============================================================

if prompt:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.session_state.total_questions += 1

    # Show user message
    with st.chat_message("user"):

        st.markdown(prompt)

    # ========================================================
    # AI RESPONSE
    # ========================================================

    with st.chat_message("assistant"):

        if client is None:

            st.error(
                "❌ Groq API key is missing.\n\n"
                "Add this to `.streamlit/secrets.toml`:\n\n"
                "```toml\n"
                'GROQ_API_KEY = "your-api-key"\n'
                "```"
            )

        elif not st.session_state.get("groq_model"):

            st.error(
                "❌ No compatible Groq model was found "
                "for your API key."
            )

        else:

            try:

                response = client.chat.completions.create(
                    model=st.session_state.groq_model,
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=2048
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"❌ Groq Error:\n\n{str(e)}"
                )
