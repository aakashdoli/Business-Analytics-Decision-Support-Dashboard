import streamlit as st
from app.ai_insights.copilot import AICopilot
from app.utils.styles import apply_custom_styles
from app.utils.navigation import render_top_nav

st.set_page_config(page_title="AI Co-Pilot", layout="wide", initial_sidebar_state="collapsed")
apply_custom_styles()
render_top_nav()

st.markdown("# 🤖 Enterprise AI Co-Pilot")
st.markdown('<div style="font-size:.88rem;color:#64748B;margin-bottom:1.5rem;">Semantic operational intelligence · Multi-step reasoning · Executive-grade analysis</div>', unsafe_allow_html=True)

# ── Init ───────────────────────────────────────────────────────────────────────
if 'copilot' not in st.session_state:
    st.session_state.copilot = AICopilot()
if 'messages' not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "I am your **Enterprise Data Co-Pilot** — an AI reasoning engine connected directly to your operational data warehouse.\n\n"
            "I can analyse **cost drivers**, **regional performance**, **anomaly incidents**, **workforce productivity**, and **revenue trends** with executive-grade precision.\n\n"
            "What would you like to investigate today?"
        ),
        "follow_ups": [
            "What is driving our highest operational costs?",
            "Give me an executive health overview",
            "Explain recent anomaly incidents",
            "Which region has the best operating margin?"
        ]
    }]

# ── Render chat history ────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"],
                         avatar="🤖" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

        # Render follow-up buttons only for the latest assistant message
        if (msg["role"] == "assistant"
                and msg.get("follow_ups")
                and msg is st.session_state.messages[-1]):
            st.markdown('<div style="margin-top:.6rem;font-size:.75rem;color:#475569;font-weight:600;">SUGGESTED ANALYSIS</div>', unsafe_allow_html=True)
            ncols = min(len(msg["follow_ups"]), 4)
            cols = st.columns(ncols)
            for idx, suggestion in enumerate(msg["follow_ups"][:ncols]):
                with cols[idx]:
                    if st.button(suggestion, key=f"sug_{idx}_{len(st.session_state.messages)}",
                                 use_container_width=True):
                        st.session_state.pending_query = suggestion
                        st.rerun()

# ── Input handling ─────────────────────────────────────────────────────────────
query = st.chat_input("Ask your operational data anything...")

if 'pending_query' in st.session_state:
    query = st.session_state.pop('pending_query')

if query:
    # User bubble
    with st.chat_message("user", avatar="👤"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # Assistant response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analysing operational warehouse..."):
            res = st.session_state.copilot.ask(query)
        st.markdown(res['response'])
        st.session_state.messages.append({
            "role": "assistant",
            "content": res['response'],
            "follow_ups": res.get('follow_ups', [])
        })
    st.rerun()
