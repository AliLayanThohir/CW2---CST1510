#Importing needed libraries for application
import streamlit as st

#Configuration of the page, title of website, icon and layout
st.set_page_config(page_title="Login / Register", page_icon="🔑",layout="centered")

#Intializing session 
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🔐 Welcome")