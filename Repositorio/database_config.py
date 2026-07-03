"""
Autor: Angelo Francisco da Silva
Data: 03/07/2026
Projeto: AuQMiaSis
"""

import psycopg2
import streamlit as st
from urllib.parse import quote_plus

@st.cache_resource
def get_connection_cached():
    return obter_conexao()

def obter_conexao():
    try:
        db = st.secrets["database"]
        
        # Conectando usando dicionário de argumentos (mais robusto)
        conn = psycopg2.connect(
            host=db["host"],
            database=db["dbname"],
            user=db["user"],
            password=db["password"],
            port=db["port"],
            sslmode="require", # O Supabase EXIGE SSL
            connect_timeout=10
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")
        return None