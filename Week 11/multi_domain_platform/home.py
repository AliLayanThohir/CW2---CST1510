#Importing libraries / needed items to run homepage
import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from utils.navigation import make_sidebar

#Page configuration, icon, title and it's layout
st.set_page_config(page_title="Intelligence Platform", page_icon="🔐", layout="centered")

#Initialize Services
db = DatabaseManager()
auth = AuthManager(db)

#Function to setup database
@st.cache_resource
def system_startup():
    print("--- Initializing Database Setup ---")
    db.create_tables()
    print("--- Database Setup Complete ---")

#Run the setup once when the script starts
system_startup()

#Initializing session state variables if they don't exist yet
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

#Render Sidebar (Custom implementation based on your Utils)
with st.sidebar:
    st.title("🧩 Navigation")
    st.page_link("Home.py", label="Home", icon="🏠")
    
    if st.session_state.logged_in:
        st.subheader("Modules")
        st.page_link("pages/1_🔐 _Login.py", label="Dashboard", icon="📊")
        
        #Variable needed to check what role the logged in user current is
        role = st.session_state.role
        
        #Shows the Cybersecurity page - Only to Cybersecurity Analysts
        if role == "Cybersecurity Analyst":
            st.page_link("pages/2_🛡️ _Cybersecurity.py", label="Cybersecurity", icon="🛡️")
        
        #Shows the Data Science page - Only to Data Scientists
        if role == "Data Scientist":
            st.page_link("pages/3_📊 _Data_Science.py", label="Data Science", icon="📊")
            
        #Shows the IT Operations page - Only to IT Administrators
        if role == "IT Administrator":
            st.page_link("pages/4_💻 _IT_Operations.py", label="IT Operations", icon="💻")
        
        #Shows the AI Assistant page - Available to all roles    
        st.page_link("pages/5_🤖 _AI_Assistant.py", label="AI Assistant", icon="🤖")
        
        st.divider()
        if st.button("Log Out", use_container_width=True):
            #Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.success("Logged out successfully!")
            st.rerun()
    elif st.session_state.logged_in is False:
        st.info("Please log in to access modules.")

#Title for the main page
st.title("🔐 Multi-Domain Intelligence Platform")

#If user is logged in
if st.session_state.logged_in:
    st.success(f"You are currently logged in as **{st.session_state.username}** ({st.session_state.role}).")
    st.info("Use the sidebar 🧭 to navigate to your modules.")

#If user is not logged in
else:
    st.write("Welcome! Please login or register to access the dashboard.")
    #Menu/Start-up display for registration/login
    tab1, tab2 = st.tabs(["Login", "Register"])

    #If user wants to login to an existing account
    with tab1:
        st.header("Login")
        #Username
        login_user_input = st.text_input("Username", key="login_user")
        #Password
        login_pass_input = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Log In", type="primary"):
            #Check if inputs are provided
            if login_user_input and login_pass_input:
                #Login user function using predefined function
                user, msg = auth.login_user(login_user_input, login_pass_input)
                
                #If login successful, updates session state and redirects
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user.get_username()
                    st.session_state.role = user.get_role()
                    st.success(msg)
                    st.switch_page("pages/1_🔐 _Login.py")
                #If unsuccessful displays error message
                else:
                    st.error(msg)
            #If fields are empty
            else:
                st.warning("Please enter both username and password.")

    #If user wants to register a new account
    with tab2:
        #Display of function
        st.header("Register")
        
        #Username
        reg_user_input = st.text_input("Choose Username", key="reg_user")
        #Password
        reg_pass_input = st.text_input("Choose Password", type="password", key="reg_pass")
        reg_confirm_input = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        #Group to be assigned to
        group_choice = st.selectbox(
            "Select Department",
            ("Cybersecurity Analyst", "Data Scientist", "IT Administrator")
        )
        
        if st.button("Create Account"):
            #Check for empty fields
            if not reg_user_input or not reg_pass_input:
                st.warning("Please fill in all fields.")
            
            #Check for password mismatch
            elif reg_pass_input != reg_confirm_input:
                st.error("Passwords do not match.")
            
            else:
                #Validation check for username using predefined function
                valid_user, user_msg = auth.validate_user(reg_user_input)
                
                #If username is invalid
                if not valid_user:
                    st.error(user_msg)
                else:
                    #Validation check for password using predefined function
                    valid_pass, pass_msg = auth.validate_pass(reg_pass_input)
                    
                    #If password is invalid
                    if not valid_pass:
                        st.error(pass_msg)
                    else:
                        #Password strength check using predefined function
                        strength = auth.check_password_strength(reg_pass_input)
                        
                        #If password strength is not strong
                        if strength != "Strong":
                            st.warning(f"Password Strength: {strength}")
                            st.info("Password must be Strong (Min 12 chars, Upper, Lower, Digit, Special).")
                        else:
                            #If all validations are passed, registers user and prints confirmation
                            success, msg = auth.register_user(reg_user_input, reg_pass_input, group_choice)
                            
                            if success:
                                st.success(msg + " Please switch to the Login tab.")
                            else:
                                st.error(msg)