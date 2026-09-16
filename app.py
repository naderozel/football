import streamlit as st
from groq import Groq

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Football AI Chatbot",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .main {
        background-color: #f7f9fc;
    }

    .football-title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        color: #0b5d1e;
        margin-bottom: 5px;
    }

    .football-subtitle {
        text-align: center;
        font-size: 20px;
        color: #555;
        margin-bottom: 30px;
    }

    .category-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e5e5e5;
        margin-bottom: 15px;
    }

    .category-card:hover {
        border-color: #0b5d1e;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
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
# FOOTBALL SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are Football AI, a friendly and knowledgeable football chatbot.

Your job is to talk primarily about association football (soccer).

You can discuss:

1. Football rules
2. Football tactics
3. Football formations
4. Clubs
5. National teams
6. Players
7. Managers and coaches
8. Football history
9. Major competitions
10. Domestic leagues
11. Champions League
12. Europa League
13. World Cup
14. Women's football
15. Youth football
16. Football transfers
17. Player statistics
18. Team statistics
19. Famous matches
20. Football terminology
21. Training and skills
22. Positions on the pitch
23. Goalkeeping
24. Defending
25. Midfield
26. Attacking
27. Set pieces
28. Penalties
29. Offside
30. VAR
31. Football culture

Explain football topics clearly and accurately.

When appropriate, use:
- Short sections
- Bullet points
- Examples
- Tables
- Tactical explanations

If the user asks about something unrelated to football,
politely explain that you are a football-focused chatbot and
ask them to ask a football-related question.

Do not claim to have live information unless it is actually
provided to you.

If the user asks about current scores, fixtures, standings,
transfers, injuries, or other information that changes
frequently, clearly explain that current information should
be verified using a reliable live source.

Be friendly, enthusiastic, and informative.

You may use football emojis such as ⚽ 🥅 🏆 🔥.
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

    st.write(
        "Your personal chatbot for learning and talking about football."
    )

    

    st.divider()

    st.subheader("💬 Example Questions")

    example_questions = [
        "What is the offside rule?",
        "Explain the 4-3-3 formation.",
        "What does a defensive midfielder do?",
        "How does VAR work?",
        "What are the main football positions?",
        "Explain the Champions League.",
        "What makes a good striker?",
        "What is a false nine?"
    ]

    for i, question in enumerate(example_questions):

        if st.button(
            question,
            key=f"example_{i}"
        ):
            st.session_state.pending_question = question
            st.rerun()

    st.divider()

    st.subheader("📊 Statistics")

    st.metric(
        "Questions Asked",
        st.session_state.total_questions
    )

    if st.button("🗑️ Clear Chat"):

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

    st.caption("⚽ Football AI • Built with Streamlit + Groq")

# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="football-title">⚽ Football AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="football-subtitle">'
    'Ask questions about football, tactics, players, clubs, '
    'competitions and more.'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# WELCOME SECTION
# ============================================================

if len(st.session_state.messages) == 1:

    st.info(
        "👋 Welcome! I am Football AI. "
        "Ask me anything about football."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="category-card" style="color:black;">
        <h3>🏆 Competitions</h3>
        <p>
        Learn about the World Cup, Champions League,
        domestic leagues and international tournaments.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="category-card" style="color:black;">
        <h3>📋 Tactics</h3>
        <p>
        Learn about formations, pressing, possession,
        counter-attacks and defensive systems.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="category-card" style="color:black;">
        <h3>👤 Players</h3>
        <p>
        Ask about football positions, player roles,
        skills and famous footballers.
        </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================================
# GET SIDEBAR QUESTION
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

# Sidebar question takes priority
if pending_question:
    prompt = pending_question

# ============================================================
# PROCESS USER QUESTION
# ============================================================

if prompt:

    # --------------------------------------------------------
    # ADD USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.session_state.total_questions += 1

    # --------------------------------------------------------
    # DISPLAY USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message("user"):
        st.markdown(prompt)

    # --------------------------------------------------------
    # GENERATE AI RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        if client is None:

            st.error(
                "⚠️ Groq API key is missing. "
                "Please configure GROQ_API_KEY in "
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

                # ------------------------------------------------
                # SAVE ASSISTANT RESPONSE
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"❌ An error occurred while contacting Groq:\n\n"
                    f"`{str(e)}`"
                )
