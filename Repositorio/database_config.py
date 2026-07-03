"""
Autor: Angelo Francisco da Silva
Data: 02/07/2026
Projeto: AuQMiaSis
"""

import psycopg2
import streamlit as st
from urllib.parse import quote_plus

@st.cache_resource
def get_connection_cached():
    return obter_conexao()

def obter_conexao():
    """
    Centraliza a conexão com o banco de dados PostgreSQL (Supabase)
    usando os parâmetros do st.secrets.
    """
    try:
        db = st.secrets["database"]
        senha_segura = quote_plus(db["password"])
        
        # Monta a URI usando as variáveis do arquivo secrets
        DB_URI = f"postgresql://{db['user']}:{senha_segura}@{db['host']}:{db['port']}/{db['dbname']}"
        
        return psycopg2.connect(DB_URI)
    except Exception as e:
        st.error(f"Erro crítico ao conectar ao banco de dados: {e}")
        return None

        