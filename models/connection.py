import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_NAME")
USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DRIVER = os.getenv("DB_DRIVER")
TRUST_CERT = os.getenv("TRUST_CERT", "no")  # Por defecto "no"

password_encoded = urllib.parse.quote_plus(PASSWORD)

# Agregar TrustServerCertificate si es necesario
if TRUST_CERT.lower() == "yes":
    connection_string = f"mssql+pyodbc://{USERNAME}:{password_encoded}@{SERVER}/{DATABASE}?driver={DRIVER}&TrustServerCertificate=yes"
else:
    connection_string = f"mssql+pyodbc://{USERNAME}:{password_encoded}@{SERVER}/{DATABASE}?driver={DRIVER}"

@st.cache_resource
def init_connection():
    try:
        engine = create_engine(connection_string)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        st.success("✅ Conexión exitosa")
        return engine
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

# Resto del código...
st.title("📊 SQL Server")
engine = init_connection()