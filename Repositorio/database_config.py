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
    Centraliza a conexão com o banco de dados PostgreSQL (Supabase).
    Busca a senha de forma segura a partir do st.secrets.
    """
    try:
        senha_pura = st.secrets["database"]["password"]
        senha_segura = quote_plus(senha_pura)
        DB_URI = f"postgresql://postgres:{senha_segura}@db.zpnxtrmbpnenuulidrwl.supabase.co:5432/postgres"
        return psycopg2.connect(DB_URI)
    except Exception as e:
        st.error(f"Erro crítico ao conectar ao banco de dados: {e}")
        return None

        