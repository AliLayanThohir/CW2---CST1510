#Importing libraries / needed items to show data science interface
import streamlit as st
import pandas as pd
from datetime import date, datetime
from services.database_manager import DatabaseManager
from models.dataset import Dataset
from utils.navigation import make_sidebar

##Page configuration, icon, title and it's layout
st.set_page_config(page_title="Data Science", page_icon="📈", layout="wide")

#Render the custom sidebar
make_sidebar()

#Security Check
if st.session_state.get("role") != "Data Scientist":
    st.error("⛔ Access Restricted: Data Scientists Only.")
    st.stop()

#Initialize DB
db = DatabaseManager()

#Page title
st.title("📈 Data Science Hub")

#Splits into two different columns
col1, col2 = st.columns([2, 1])

#Allows for viewage of Datasets, shows table with all data
with col1:
    st.subheader("Available Datasets")
    rows = db.fetch_all("SELECT * FROM datasets_metadata ORDER BY id DESC")
    datasets = [Dataset(*row) for row in rows]
    
    if datasets:
        df = pd.DataFrame([d.to_dict() for d in datasets])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No datasets found.")

#Section to add new datasets
with col2:
    #Subheader for adding
    st.subheader("Add New Dataset")
    with st.form("dataset_form"):
        ds_name = st.text_input("Dataset Name") #Name of the dataset
        ds_cat = st.selectbox("Category", ["Financial", "Operational", "Customer", "Security"]) #Category of the dataset
        ds_source = st.text_input("Source") #Source where data came from
        ds_date = st.date_input("Last Updated", value=date.today()) #Automatically puts current date
        ds_count = st.number_input("Record Count", min_value=0) #Count of records
        ds_size = st.number_input("Size (MB)", min_value=0.0, format="%.2f") #Size of the file
        
        #Button so the dataset is added
        if st.form_submit_button("Add Dataset"):
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #Inserts dataset data
            db.execute_query(
                "INSERT INTO datasets_metadata (dataset_name, category, source, last_updated, record_count, file_size_mb, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (ds_name, ds_cat, ds_source, str(ds_date), ds_count, ds_size, created_at)
            )
            st.success("Dataset added.") #Print message to show that it has been added
            st.rerun() #Refreshes automatically so table is updated

#Seperator for page format
st.divider()

#Section to manage datasets
st.subheader("Manage Datasets")

#Only shows up if data exists
if datasets:
    #Selection of which dataset by it's ID number
    selected_id = st.selectbox("Select Dataset ID", [d.get_id() for d in datasets])
    #Find selected object
    current_ds = next((d for d in datasets if d.get_id() == selected_id), None)
    
    #Splits to two sections, update or delete
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        with st.form("upd_form"):
            #For updating count of the records
            new_count = st.number_input("New Record Count", value=int(current_ds.record_count) if current_ds else 0)
            if st.form_submit_button("Update Count"):
                db.execute_query("UPDATE datasets_metadata SET record_count = ? WHERE id = ?", (new_count, selected_id))
                st.success("Updated.") #Print message to show it updated
                st.rerun() #Refreshes automatically so table is updated
    with col_m2:
        st.write("Delete")
        if st.button("Delete Dataset", type="primary"):
            db.execute_query("DELETE FROM datasets_metadata WHERE id = ?", (selected_id,))
            st.rerun() #Refreshes automatically so table is updated