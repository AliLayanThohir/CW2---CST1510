#Importing libraries / needed items to show dashboard interface
import streamlit as st
from app.data.incidents import get_all_incidents
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets
from app.utils.navigation import make_sidebar

##Page configuration, Icon, Title and it's layout
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

#If user isn't logged in, show error message and stop
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("⛔ You must be logged in to view this page.")
    st.stop()

#Creates sidebar 
make_sidebar()

#Creates title and welcome message 
st.title("📊 Executive Overview")
st.write(f"Welcome back, **{st.session_state.username}**.")

#Gets data from all of the databases
df_incidents = get_all_incidents()
df_datasets = get_all_datasets()
df_tickets = get_all_tickets()

#Page format to display data
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Incidents", value=len(df_incidents))
with col2:
    total_size = df_datasets['file_size_mb'].sum() if not df_datasets.empty else 0
    st.metric(label="Data Volume (MB)", value=f"{total_size:.2f}")
with col3:
    open_tickets = len(df_tickets[df_tickets['status'] == 'Open']) if not df_tickets.empty else 0
    st.metric(label="Open IT Tickets", value=open_tickets)

#Divider for page format
st.divider()

#Subheader for chart datsa 
st.subheader("System Activity")
#Page format for charts
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.caption("Incidents by Severity")
    if not df_incidents.empty:
        st.bar_chart(df_incidents['severity'].value_counts())
with chart_col2:
    st.caption("Tickets by Status")
    if not df_tickets.empty:
        st.bar_chart(df_tickets['status'].value_counts())