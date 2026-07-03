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
        # Acessa o dicionário de configurações
        db = st.secrets["database"]
        
        # Extrai e limpa os dados
        user = str(db["user"]).strip()
        pwd = quote_plus(str(db["password"]).strip())
        host = str(db["host"]).strip()
        port = str(db["port"]).strip()
        dbname = str(db["dbname"]).strip()
        
        # Monta a URI
        DB_URI = f"postgresql://{user}:{pwd}@{host}:{port}/{dbname}"
        
        # Tenta conectar
        conn = psycopg2.connect(DB_URI, connect_timeout=10)
        return conn
        
    except Exception as e:
        # Isso vai aparecer na tela do seu celular se der erro
        st.error(f"Erro ao conectar: {type(e).__name__} - {e}")
        return None