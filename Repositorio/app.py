"""
Autor: Angelo Francisco da Silva
Data: 03/07/2026
Projeto: AuQMiaSis
"""

import streamlit as st
from database_config import obter_conexao
from modulos.usuarios.usuarios_view import tela_usuarios
from modulos.clientes.clientes_view import tela_clientes

# 1. FUNÇÃO PARA INICIALIZAR TABELAS
def inicializar_banco():
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            # Tabelas estruturadas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY, usuario TEXT UNIQUE NOT NULL, senha TEXT NOT NULL, nivel TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS clientes (id SERIAL PRIMARY KEY, nome TEXT, apelido TEXT, telefone TEXT, endereco TEXT, usa_frete TEXT, valor_frete REAL);
                CREATE TABLE IF NOT EXISTS pets (id SERIAL PRIMARY KEY, cliente_id INTEGER, nome_pet TEXT, classe TEXT, raca TEXT, FOREIGN KEY(cliente_id) REFERENCES clientes(id));
                CREATE TABLE IF NOT EXISTS servicos (id SERIAL PRIMARY KEY, descricao TEXT, valor REAL, valor_pacote REAL);
                CREATE TABLE IF NOT EXISTS agendamentos (id SERIAL PRIMARY KEY, pet_id INTEGER, servico_id INTEGER, data_hora TEXT, status TEXT, FOREIGN KEY(pet_id) REFERENCES pets(id), FOREIGN KEY(servico_id) REFERENCES servicos(id));
                CREATE TABLE IF NOT EXISTS fichas_entrada (id SERIAL PRIMARY KEY, pet_id INTEGER, condicao_geral TEXT, data_registro TEXT, foto TEXT, FOREIGN KEY(pet_id) REFERENCES pets(id));
                CREATE TABLE IF NOT EXISTS movimentacao (id SERIAL PRIMARY KEY, pet_id INTEGER, agendamento_id INTEGER, servico_id INTEGER, valor_servico REAL, valor_frete REAL, data_pagamento TEXT, status_pagamento TEXT);
                CREATE TABLE IF NOT EXISTS financeiro_geral (id SERIAL PRIMARY KEY, tipo TEXT, descricao TEXT, valor REAL, data_vencimento TEXT, status TEXT);
                CREATE TABLE IF NOT EXISTS pacotes_vendidos (id SERIAL PRIMARY KEY, cliente_id INTEGER, nome_pacote TEXT, valor_total REAL, data_venda TEXT);
                CREATE TABLE IF NOT EXISTS itens_pacote (id SERIAL PRIMARY KEY, pacote_vendido_id INTEGER, servico_id INTEGER, qtd_total INTEGER, qtd_usada INTEGER);
            ''')
            
            # Criar admin padrão
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO usuarios (usuario, senha, nivel) VALUES (%s, %s, %s)", ('admin', 'admin123', 'Administrador'))
                
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Erro ao inicializar tabelas: {e}")

# Executa inicialização
inicializar_banco()

# 2. CONTROLE DE SESSÃO
if 'logado' not in st.session_state:
    st.session_state['logado'] = False
    st.session_state['usuario_atual'] = ""

# 3. TELA DE LOGIN
if not st.session_state['logado']:
    st.markdown("<h2 style='text-align: center;'>🐾 Banho e Tosa - Acesso Online</h2>", unsafe_allow_html=True)
    with st.form("tela_login"):
        usuario_input = st.text_input("Usuário")
        senha_input = st.text_input("Senha", type="password")
        botao_entrar = st.form_submit_button("Entrar no Sistema")
        
        if botao_entrar:
            conn = obter_conexao()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nivel FROM usuarios WHERE usuario = %s AND senha = %s", (usuario_input, senha_input))
                resultado = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if resultado:
                    st.session_state['logado'] = True
                    st.session_state['usuario_atual'] = usuario_input
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos!")

# 4. AMBIENTE LOGADO
else:
    st.sidebar.title(f"Olá, {st.session_state['usuario_atual']}!")
    menu_opcao = st.sidebar.selectbox("Navegação", ["Início / Painel", "Usuários", "Clientes e Pets"])
    
    if st.sidebar.button("Sair / Logout"):
        st.session_state['logado'] = False
        st.rerun()
        
    if menu_opcao == "Início / Painel":
        st.title("🐾 Painel Principal")
        st.success("Conectado com sucesso ao banco de dados Aiven!")
    elif menu_opcao == "Usuários":
        tela_usuarios()
    elif menu_opcao == "Clientes e Pets":
        tela_clientes()