#Importing libraries / needed items to show cybersecurity interface
import streamlit as st 
import pandas as pd
from datetime import date, datetime 
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident
from utils.navigation import make_sidebar

#Page configuration, icon, title and it's layout
st.set_page_config(page_title="Cybersecurity", page_icon="🔒", layout="wide")

#Render the custom sidebar
make_sidebar()

#Security Check
if st.session_state.get("role") != "Cybersecurity Analyst":
    st.error("⛔ Access Restricted: Cybersecurity Analysts Only.")
    st.stop()

#Initialize DB
db = DatabaseManager()

#Page title
st.title("🔒 Cybersecurity Operations") 

#Creates tabs for each action
tab_view, tab_analytics, tab_add, tab_manage = st.tabs(["View Log", "Analytics", "Report Incident", "Manage Records"]) 

#Allows for viewage of Log data, shows table with all data
with tab_view:
    st.subheader("Incident Log") 
    
    """Fetch rows via manager."""
    rows = db.fetch_all("SELECT * FROM cyber_incidents ORDER BY id DESC")
    incidents = [SecurityIncident(*row) for row in rows]
    
    if incidents:
        #Convert back to DF for display
        df = pd.DataFrame([i.to_dict() for i in incidents])
        st.dataframe(df, use_container_width=True) 
    else:
        st.info("No incidents found.")

#Shows analytical data of all the incidents
with tab_analytics: 
    st.subheader("Incident Analytics") 
    #Splits into two different columns
    col1, col2 = st.columns(2) 
    with col1:
        #Bar chart with type of incidents
        st.markdown("**Incidents by Type**") 
        df_type = db.get_dataframe("SELECT incident_type, COUNT(*) as count FROM cyber_incidents GROUP BY incident_type ORDER BY count DESC")
        if not df_type.empty:
             st.bar_chart(df_type.set_index("incident_type")) 
    with col2:
        #Shows data table of incidents by their severity: only shows High and Critical status incidents
        st.markdown("**High Severity by Status**") 
        df_high = db.get_dataframe("SELECT status, COUNT(*) as count FROM cyber_incidents WHERE severity = 'High' OR severity = 'Critical' GROUP BY status ORDER BY count DESC")
        st.dataframe(df_high, use_container_width=True) 

#Tab to add incidents
with tab_add: 
    #Subheader for adding
    st.subheader("Report New Incident") 
    with st.form("incident_form"): 
        inc_date = st.date_input("Date", value=date.today()) #Automatically puts current date for incident
        inc_type = st.selectbox("Type", ["Phishing", "Malware", "DDoS", "Intrusion", "Other"]) #What type of incident
        inc_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"]) #Severity of the incident
        inc_status = st.selectbox("Status", ["Open", "Investigating", "Resolved"]) #Status of the incident
        inc_desc = st.text_area("Description") #Description of the incident
        
        #Button so the incident is logged
        if st.form_submit_button("Submit Report"):
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #Inserts incident data via DatabaseManager
            db.execute_query(
                "INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (str(inc_date), inc_type, inc_severity, inc_status, inc_desc, st.session_state.username, created_at)
            )
            st.success("Incident reported successfully!") #Print message to show that it has been logged
            st.rerun() #Refreshes automatically so table is updated

#Tab to manage incidents
with tab_manage: 
    st.subheader("Manage Incidents") 
    rows = db.fetch_all("SELECT * FROM cyber_incidents ORDER BY id DESC")
    incidents = [SecurityIncident(*row) for row in rows]
    
    #Only shows up if data exists
    if incidents: 
        #Selection of which incident by it's ID number
        incident_id = st.selectbox("Select Incident ID", [i.get_id() for i in incidents]) 
        #Splits to two sections, update or delete
        col_up, col_del = st.columns(2) 
        with col_up:
            #For updating status of the incident
            new_status = st.selectbox("New Status", ["Open", "Investigating", "Resolved"], key="stat") 
            if st.button("Update Status"):
                db.execute_query("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
                st.success("Status updated.") 
                st.rerun() #Refreshes automatically so table is updated
        with col_del:
            if st.button("Delete Incident", type="primary"): 
                db.execute_query("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
                st.rerun() #Refreshes automatically so table is updated