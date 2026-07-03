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
        # Acessa a URL completa do Aiven
        db_url = st.secrets["database"]["url"]
        
        # Conecta usando a URL direta
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        st.error(f"Erro de conexão com Aiven: {e}")
        return None