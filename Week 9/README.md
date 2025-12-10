# Week 9: Streamlit Web Interface & GUI
Student Name: Ali Layan Thohir
Student ID: M01091333
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description
This project marks the transition from the command-line interface (Week 8) to a web-based Graphical User Interface (GUI) using Streamlit. The application implements the full functionality of the intelligence platform—authentication, dashboard analytics, and domain-specific operations—within an interactive web environment.

## Features
- **Web-Based GUI**: Replaces the CLI with a responsive web interface.
- **Visual Dashboard**: Displays real-time metrics and charts for system activity.
- **Secure Authentication**: Web forms for Login and Registration with session state management.
- **Interactive Data Management**: Tables and forms to View, Add, Update, and Delete records.
- **Role-Based Views**: Sidebar navigation that adapts based on the logged-in user's role.

## Technical Implementation
- **Interface**: Streamlit framework (`st.sidebar`, `st.columns`, `st.tabs`).
- **Data Visualization**: Streamlit charts (`bar_chart`, `metric`) and Pandas DataFrames.
- **State Management**: Uses `st.session_state` to handle login status and user sessions across pages.
- **Database Access**: Direct functional calls to SQLite via `app.data` modules.
- **Application Structure**:
    - `home.py`: Main entry point handling authentication.
    - `pages/`: Individual pages for Dashboard, Cybersecurity, Data Science, and IT Operations.
    - `app/data/`: Backend modules for handling database operations.
