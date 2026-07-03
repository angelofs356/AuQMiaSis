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
        # Acessa as configurações que você colocou no Secrets
        db = st.secrets["database"]
        
        # Conecta via porta 6543 (Transaction Mode)
        conn = psycopg2.connect(
            host=db["host"],
            database=db["dbname"],
            user=db["user"],
            password=db["password"],
            port=db["port"],
            sslmode="require"
        )
        return conn
    except Exception as e:
        # Se falhar, vamos ver exatamente o que é
        st.error(f"Erro detalhado: {e}")
        return None