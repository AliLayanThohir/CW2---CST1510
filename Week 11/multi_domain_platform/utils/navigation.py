#Importing libraries needed for navigation
import streamlit as st
from time import sleep

#Function to create the custom sidebar
def make_sidebar():
    with st.sidebar:
        #Title of the sidebar
        st.title("🧩 Navigation")
        
        #Page switch to go back to homepage
        st.page_link("Home.py", label="Home", icon="🏠")
        
        #Check if user is logged in
        if st.session_state.get("logged_in", False):
            
            #Subheader for modules
            st.subheader("Modules")
            
            #Dashboard link 
            st.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")
            
            #Get current user role
            role = st.session_state.get("role", "")
            
            #Shows the Cybersecurity page - Only to Cybersecurity Analysts
            if role == "Cybersecurity Analyst":
                st.page_link("pages/2_Cybersecurity.py", label="Cybersecurity", icon="🔒")
            
            #Shows the Data Science page - Only to Data Scientists
            if role == "Data Scientist":
                st.page_link("pages/3_Data_Science.py", label="Data Science", icon="📈")
                
            #Shows the IT Operations page - Only to IT Administrators
            if role == "IT Administrator":
                st.page_link("pages/4_IT_Operations.py", label="IT Operations", icon="⚙️")
            
            #Always show the AI Assistant
            st.page_link("pages/5_AI_Assistant.py", label="AI Assistant", icon="🤖")
            
            #Logout Section
            st.divider()
            if st.button("Log Out", use_container_width=True):
                #Clear session state variables
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.role = ""
                
                #Clear any service instances (like AI assistant)
                if 'ai_service' in st.session_state:
                    del st.session_state['ai_service']
                
                st.success("Logged out successfully!")
                sleep(0.5)
                st.switch_page("Home.py")
        
        #If the user isn't logged in
        elif st.session_state.get("logged_in") is False:
            st.info("Please log in to access modules.")