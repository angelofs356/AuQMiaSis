import streamlit as st
import psycopg2
from psycopg2 import extras
from urllib.parse import quote_plus

# IMPORTAÇÃO DA VIEW QUE CRIAMOS
from modulos.usuarios.usuarios_view import tela_usuarios

# BUSCA A SENHA COM SEGURANÇA DO ARQUIVO SECRETS (ELAS NÃO FICAM NO CÓDIGO-FONTE)
senha_pura = st.secrets["database"]["password"]
senha_segura = quote_plus(senha_pura)

# 1. CONEXÃO COM O BANCO DE DADOS POSTGRESQL (SUPABASE)
DB_URI = f"postgresql://postgres:{senha_segura}@db.zpnxtrmbpnenuulidrwl.supabase.co:5432/postgres"

def inicializar_banco():
    try:
        conn = psycopg2.connect(DB_URI)
        cursor = conn.cursor()
        
        # Criando a tabela de usuários estruturada na nuvem
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                nivel TEXT NOT NULL
            )
        ''')
        
        # Criando as demais tabelas que você projetou
        cursor.execute('CREATE TABLE IF NOT EXISTS clientes (id SERIAL PRIMARY KEY, nome TEXT, apelido TEXT, telefone TEXT, endereco TEXT, usa_frete TEXT, valor_frete REAL)')
        cursor.execute('CREATE TABLE IF NOT EXISTS pets (id SERIAL PRIMARY KEY, cliente_id INTEGER, nome_pet TEXT, classe TEXT, raca TEXT, FOREIGN KEY(cliente_id) REFERENCES clientes(id))')
        cursor.execute('CREATE TABLE IF NOT EXISTS servicos (id SERIAL PRIMARY KEY, descricao TEXT, valor REAL, valor_pacote REAL)')
        cursor.execute('CREATE TABLE IF NOT EXISTS agendamentos (id SERIAL PRIMARY KEY, pet_id INTEGER, servico_id INTEGER, data_hora TEXT, status TEXT, FOREIGN KEY(pet_id) REFERENCES pets(id), FOREIGN KEY(servico_id) REFERENCES servicos(id))')
        cursor.execute('CREATE TABLE IF NOT EXISTS fichas_entrada (id SERIAL PRIMARY KEY, pet_id INTEGER, condicao_geral TEXT, data_registro TEXT, foto TEXT, FOREIGN KEY(pet_id) REFERENCES pets(id))')
        cursor.execute('CREATE TABLE IF NOT EXISTS movimentacao (id SERIAL PRIMARY KEY, pet_id INTEGER, agendamento_id INTEGER, servico_id INTEGER, valor_servico REAL, valor_frete REAL, data_pagamento TEXT, status_pagamento TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS financeiro_geral (id SERIAL PRIMARY KEY, tipo TEXT, descricao TEXT, valor REAL, data_vencimento TEXT, status TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS pacotes_vendidos (id SERIAL PRIMARY KEY, cliente_id INTEGER, nome_pacote TEXT, valor_total REAL, data_venda TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS itens_pacote (id SERIAL PRIMARY KEY, pacote_vendido_id INTEGER, servico_id INTEGER, qtd_total INTEGER, qtd_usada INTEGER)')
        
        # Criar usuário admin padrão se não houver nenhum
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO usuarios (usuario, senha, nivel) VALUES (%s, %s, %s)", ('admin', 'admin123', 'Administrador'))
            
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")

# Executa a criação das tabelas na nuvem
inicializar_banco()

# 2. CONTROLE DE SESSÃO DO USUÁRIO
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
            try:
                conn = psycopg2.connect(DB_URI)
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
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

# 4. AMBIENTE LOGADO (COM MENU DE NAVEGAÇÃO)
else:
    st.sidebar.title(f"Olá, {st.session_state['usuario_atual']}!")
    
    # Criando o menu seletor na barra lateral
    menu_opcao = st.sidebar.selectbox(
        "Navegação",
        ["Início / Painel", "Usuários", "Clientes e Pets"]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Sair / Logout"):
        st.session_state['logado'] = False
        st.session_state['usuario_atual'] = ""
        st.rerun()
        
    # Roteamento das Páginas com base no menu selecionado
    if menu_opcao == "Início / Painel":
        st.title("🐾 Painel Principal - Sistema Online")
        st.success("Conectado com sucesso ao banco de dados PostgreSQL do Supabase!")
        st.info("Utilize o menu lateral para navegar entre as funções do sistema.")
        
    elif menu_opcao == "Usuários":
        # Chama a tela modular que criamos no arquivo usuarios_view.py
        tela_usuarios()
        
    elif menu_opcao == "Clientes e Pets":
        st.title("🐾 Cadastro de Clientes e Pets")
        st.info("Esta tela será desenvolvida na próxima etapa!")