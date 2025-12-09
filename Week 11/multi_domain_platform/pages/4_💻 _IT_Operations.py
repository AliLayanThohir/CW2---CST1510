#Importing libraries / needed items to show IT Operations interface
import streamlit as st
import pandas as pd
from datetime import datetime
from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket
from utils.navigation import make_sidebar

##Page configuration, icon, title and it's layout
st.set_page_config(page_title="IT Ops", page_icon="⚙️", layout="wide")

#Render the custom sidebar
make_sidebar()

#Security Check
if st.session_state.get("role") != "IT Administrator":
    st.error("⛔ Access Restricted: IT Administrators Only.")
    st.stop()

#Initialize DB
db = DatabaseManager()

#Page title
st.title("⚙️ IT Operations & Ticketing")

#Sidebar filters
with st.sidebar:
    st.header("Filters")
    status_filter = st.multiselect("Status", ["Open", "Closed", "Resolved"], default=["Open"]) #Filter by status

#Fetch data and use Objects
rows = db.fetch_all("SELECT * FROM it_tickets ORDER BY id DESC")
tickets = [ITTicket(*row) for row in rows]
df = pd.DataFrame([t.to_dict() for t in tickets]) if tickets else pd.DataFrame()

#Filters data based on selection
if not df.empty and status_filter:
    df = df[df['status'].isin(status_filter)]

#Allows for viewage of Tickets, shows table with all data
st.metric("Visible Tickets", len(df))
st.dataframe(df, use_container_width=True)

#Seperator for page format
st.divider()

#Creates tabs for each action
tab_new, tab_update = st.tabs(["Create Ticket", "Update/Delete"])

#Tab to create tickets
with tab_new:
    with st.form("ticket_form"):
        #Splits into two different columns
        c1, c2 = st.columns(2)
        with c1:
            t_id = st.text_input("Ticket ID") #ID of the ticket
            t_subject = st.text_input("Subject") #Subject of the ticket
            t_cat = st.selectbox("Category", ["Hardware", "Software", "Network"]) #Category of the ticket
        with c2:
            t_pri = st.selectbox("Priority", ["Low", "Medium", "High"]) #Priority of the ticket
            t_stat = st.selectbox("Status", ["Open", "In Progress", "Closed"]) #Status of the ticket
            t_assign = st.text_input("Assigned To") #Who the ticket is assigned to
        t_desc = st.text_area("Description") #Description of the ticket
        
        #Button so the ticket is created
        if st.form_submit_button("Submit"):
            success = False #Flag to track if insertion was successful
            try:
                #Refactored: Insert logic from tickets.py
                created_date = datetime.now().strftime("%Y-%m-%d")
                resolved_date = created_date if t_stat in ['Resolved', 'Closed'] else None
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                #Inserts ticket data
                db.execute_query("""
                    INSERT INTO it_tickets 
                    (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (t_id, t_pri, t_stat, t_cat, t_subject, t_desc, created_date, resolved_date, t_assign, created_at))
                
                st.success("Created.") #Print message to show that it has been created
                success = True #Mark as successful
            except Exception as e:
                st.error(f"Error creating ticket: {e}") #Print specific error message
            #Check if success is true
            if success:
                st.rerun() #Refreshes automatically so table is updated

#Tab to manage tickets
with tab_update:
    if tickets:
        #Selection of which ticket by it's ID number
        tid = st.selectbox("Select Ticket ID", [t.get_ticket_id() for t in tickets])
        
        #Splits to two sections, update or delete
        col_u, col_d = st.columns(2)
        with col_u:
            #For updating status of the ticket
            new_st = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"], key="ns")
            if st.button("Update Status"):
                #Logic for resolving date ported from tickets.py
                current_ticket = next((t for t in tickets if t.get_ticket_id() == tid), None)
                new_resolved_date = current_ticket.resolved_date
                
                if new_st in ['Resolved', 'Closed']:
                     # Only update date if not already resolved/closed or missing date
                     if current_ticket.status not in ['Resolved', 'Closed'] or not current_ticket.resolved_date:
                         new_resolved_date = datetime.now().strftime("%Y-%m-%d")
                elif new_st in ['Open', 'In Progress']:
                    # Clear resolved date if reopened
                    new_resolved_date = None
                    
                db.execute_query("UPDATE it_tickets SET status = ?, resolved_date = ? WHERE ticket_id = ?", (new_st, new_resolved_date, tid))
                st.success("Updated.") #Print message to show that it has been updated
                st.rerun() #Refreshes automatically so table is updated
        with col_d:
            if st.button("Delete Ticket", type="primary"):
                db.execute_query("DELETE FROM it_tickets WHERE ticket_id = ?", (tid,))
                st.rerun() #Refreshes automatically so table is updated