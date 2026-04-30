import streamlit as st
from app.ai_insights.copilot import AICopilot
from app.utils.styles import apply_custom_styles

st.set_page_config(page_title="AI Co-Pilot", layout="wide")
apply_custom_styles()

def show():
    st.title("🤖 AI Co-Pilot")
    st.markdown("##### Ask your business data anything. Powered by Semantic Reasoning.")
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("💡 Suggestions")
        st.info("Try these queries:")
        if st.button("Which department has highest operational cost?"):
            st.session_state.query = "Which department has highest operational cost?"
        if st.button("Why did revenue decline in March?"):
            st.session_state.query = "Why did revenue decline in March?"
        if st.button("Show anomaly trends for logistics."):
            st.session_state.query = "Show anomaly trends for logistics."
        if st.button("Best performing region?"):
            st.session_state.query = "Best performing region?"

    with col2:
        st.subheader("💬 Ask Your Data")
        
        # Session state for chat history if needed
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            
        user_query = st.text_input("Enter your business question...", 
                                   value=st.session_state.get('query', ''),
                                   key="query_input")
        
        if st.button("Send Query"):
            if user_query:
                copilot = AICopilot()
                with st.spinner("Thinking..."):
                    response = copilot.ask(user_query)
                    st.session_state.chat_history.append((user_query, response))
        
        # Display chat history
        for q, r in reversed(st.session_state.chat_history):
            st.markdown(f"**You:** {q}")
            st.markdown(f"""<div class="chat-bubble"><b>AI Co-Pilot:</b><br>{r}</div>""", unsafe_allow_html=True)
            st.markdown("---")

if __name__ == "__main__":
    show()
