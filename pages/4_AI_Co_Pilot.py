import streamlit as st
from app.ai_insights.copilot import AICopilot
from app.utils.styles import apply_custom_styles

st.set_page_config(page_title="AI Co-Pilot", layout="wide")
apply_custom_styles()

def show():
    st.title("🤖 Enterprise AI Co-Pilot")
    st.markdown("##### Semantic operational intelligence engine.")
    st.markdown("---")
    
    # Initialize Copilot & State
    if 'copilot' not in st.session_state:
        st.session_state.copilot = AICopilot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Initial greeting
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello. I am your Enterprise Data Co-Pilot. I monitor KPIs, detect anomalies, and track cost efficiency. What would you like to analyze today?",
            "follow_ups": ["What is driving our highest costs?", "Show me the best performing region", "Are there any recent anomalies?"]
        })

    # Render Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            # Render follow-up suggestions if it's the latest assistant message
            if msg["role"] == "assistant" and msg.get("follow_ups") and msg == st.session_state.messages[-1]:
                st.write("**Suggested next queries:**")
                cols = st.columns(len(msg["follow_ups"]))
                for idx, suggestion in enumerate(msg["follow_ups"]):
                    with cols[idx]:
                        if st.button(suggestion, key=f"sug_{idx}_{len(st.session_state.messages)}"):
                            st.session_state.pending_query = suggestion
                            st.rerun()

    # Input Handling
    query = st.chat_input("Ask your business data anything...")
    
    # Check if a suggestion was clicked
    if 'pending_query' in st.session_state:
        query = st.session_state.pending_query
        del st.session_state.pending_query

    if query:
        # Display User Message
        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Display Assistant Thinking
        with st.chat_message("assistant"):
            with st.spinner("Analyzing operational warehouse..."):
                res = st.session_state.copilot.ask(query)
                st.markdown(res['response'])
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": res['response'],
                    "follow_ups": res.get('follow_ups', [])
                })
        st.rerun()

if __name__ == "__main__":
    show()
