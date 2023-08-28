import streamlit as st
import sqlite3
from pathlib import Path


db_path = Path.cwd() / 'data' / 'db' / 'vivino.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute a query and fetch data
cursor.execute('SELECT * FROM regions')
data = cursor.fetchall()

# Display data in Streamlit
st.title('Countries table')
st.dataframe(data)

# Close the database connection
conn.close()
