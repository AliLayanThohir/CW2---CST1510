#Importing libraries
import streamlit as st
from services.ai_assistant import AIAssistant
from utils.navigation import make_sidebar

#Page configuration
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

#Render the custom sidebar
make_sidebar()

#Page title
st.title("🛡 AI Expert Assistant")

#Check for API Key in secrets
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API Key not found in secrets. Please configure .streamlit/secrets.toml")
    st.stop()

#Initialize AI Service in Session State, passing the current user role
if 'ai_service' not in st.session_state:
    role = st.session_state.get("role", "General")
    st.session_state.ai_service = AIAssistant(api_key=st.secrets["OPENAI_API_KEY"], role=role)

#Display current mode
st.caption(f"Current Mode: **{st.session_state.ai_service.role} Expert**")

#Sidebar controls
with st.sidebar:
    if st.button("Clear Conversation"):
        st.session_state.ai_service.clear_history()
        st.rerun()

#Display history
for message in st.session_state.ai_service.history:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

#Input
prompt = st.chat_input("Ask a question about your domain:")
if prompt:
    #Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    #Add to history
    st.session_state.ai_service.add_user_message(prompt)
    
    #Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.ai_service.get_response()
                st.markdown(response)
            except Exception as e:
                st.error(f"Error calling OpenAI: {e}")