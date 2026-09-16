import streamlit as st
from groq import Groq

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Football AI",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ULTRA COMPACT CSS
# ============================================================

st.markdown("""
<style>

    /* ---------- GLOBAL ---------- */

    .block-container {
        padding: 0.25rem 1rem 0.25rem 1rem !important;
        max-width: 1400px !important;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.1rem !important;
    }

    /* ---------- HEADER ---------- */

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
        line-height: 1;
    }

    /* ---------- CARDS ---------- */

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
        line-height: 1.1;
    }

    .category-card p {
        font-size: 11px;
        margin: 2px 0 0 0 !important;
        padding: 0 !important;
        line-height: 1.15;
    }

    /* ---------- ALERT ---------- */

    div[data-testid="stAlert"] {
        padding: 4px 8px !important;
        margin: 2px 0 !important;
        min-height: 0 !important;
    }

    /* ---------- CHAT ---------- */

    div[data-testid="stChatMessage"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-testid="stChatMessageContent"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* ---------- CHAT INPUT ---------- */

    div[data-testid="stChatInput"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* ---------- BUTTONS ---------- */

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
        line-height: 1;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        width: 240px !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding: 0.25rem 0.5rem !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        margin: 1px 0 !important;
        padding: 0 !important;
        line-height: 1.1;
    }

    section[data-testid="stSidebar"] p {
        margin: 1px 0 !important;
        padding: 0 !important;
        line-height: 1.1;
        font-size: 12px;
    }

    section[data-testid="stSidebar"] hr {
        margin: 3px 0 !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* ---------- METRIC ---------- */

    div[data-testid="stMetric"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 10px !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 18px !important;
        line-height: 1 !important;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# GROQ
# ============================================================

try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except Exception:
    client = None

# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are Football AI, a friendly and knowledgeable football chatbot.

Talk primarily about association football (soccer).

You can discuss:
- Rules
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

If the question is unrelated to football, politely say
that you are a football-focused chatbot.

Do not claim to have live information.

For current scores, fixtures, standings, transfers,
injuries, or other changing information, tell the user
that current information needs to be checked from a
reliable live source.

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
        st.markdown(message["content"])

# ============================================================
# SIDEBAR QUESTION
# ============================================================

pending_question = st.session_state.pending_question

if pending_question:
    st.session_state.pending_question = None

# ============================================================
# INPUT
# ============================================================

prompt = st.chat_input(
    "⚽ Ask a football question..."
)

if pending_question:
    prompt = pending_question

# ============================================================
# RESPONSE
# ============================================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.session_state.total_questions += 1

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        if client is None:

            st.error(
                "⚠️ Groq API key is missing. "
                "Add GROQ_API_KEY to "
                ".streamlit/secrets.toml."
            )

        else:

            try:

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=2048
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"❌ Error: {str(e)}"
                )
