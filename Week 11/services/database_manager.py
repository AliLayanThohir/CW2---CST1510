#Import needed to make this module work
import sqlite3
import pandas as pd
from database.db import DB_PATH

#Class to handle database connections and queries
class DatabaseManager:
    """Handles SQLite database connections and queries."""
    
    #Constructor to initialize the database path and connection
    def __init__(self, db_path=DB_PATH):
        self._db_path = db_path
        self._connection = None

    #Function to connect to the database
    def connect(self):
        #Checks if connection is already established
        if self._connection is None:
            self._connection = sqlite3.connect(str(self._db_path))

    #Function to close the connection
    def close(self):
        #Checks if connection exists before closing
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    #Function to execute a write query (INSERT, UPDATE, DELETE)
    def execute_query(self, sql, params=()):
        self.connect()
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        self._connection.commit()
        return cursor.lastrowid 

    #Function to fetch a single row
    def fetch_one(self, sql, params=()):
        self.connect()
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()

    #Function to fetch all rows
    def fetch_all(self, sql, params=()):
        self.connect()
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    
    #Function to convert SQL results to a pandas DataFrame
    def get_dataframe(self, sql, params=()):
        self.connect()
        #Returns data as a dataframe which is needed for charts
        return pd.read_sql_query(sql, self._connection, params=params)

    #Function that creates all the tables in the database
    def create_tables(self):
        self.connect()
        cursor = self._connection.cursor()
        
        #SQL statement to create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        #SQL statement to create cyber_incidents table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            incident_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            description TEXT,
            reported_by TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        #SQL statement to create datasets_metadata table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            category TEXT,
            source TEXT,
            last_updated TEXT NOT NULL,
            record_count INTEGER,
            file_size_mb REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        #SQL statement to create it_tickets table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL UNIQUE,
            priority TEXT,
            status TEXT DEFAULT 'Open',
            category TEXT,
            subject TEXT NOT NULL,
            description TEXT,
            created_date TEXT,
            resolved_date TEXT,
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        #SQL statement to create lockout table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lockout (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            failed_attempts INTEGER DEFAULT 0,
            last_attempt_time TIMESTAMP
        )
        """)
        
        #SQL statement to create sessions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            token TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users (username)
        )
        """)
        
        self._connection.commit()
        print("✅ All tables checked/created successfully!")