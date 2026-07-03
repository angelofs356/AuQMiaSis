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
        
        # Conexão usando parâmetros individuais (mais estável que URI)
        conn = psycopg2.connect(
            dbname=db["dbname"].strip(),
            user=db["user"].strip(),
            password=db["password"].strip(),
            host=db["host"].strip(),
            port=db["port"].strip(),
            connect_timeout=10
        )
        return conn
        
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")
        return None