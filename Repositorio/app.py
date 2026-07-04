"""
Autor: Angelo Francisco da Silva
Data: 03/07/2026
Projeto: AuQMiaSis
"""

import os
import streamlit as st
import streamlit.components.v1 as components
from database_config import obter_conexao
from modulos.usuarios.usuarios_view import tela_usuarios
from modulos.clientes.clientes_view import tela_clientes

# 1. FUNÇÃO PARA INICIALIZAR BANCO
def inicializar_banco():
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY, usuario TEXT UNIQUE NOT NULL, senha TEXT NOT NULL, nivel TEXT NOT NULL);''')
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO usuarios (usuario, senha, nivel) VALUES (%s, %s, %s)", ('admin', 'admin123', 'Administrador'))
            conn.commit()
            cursor.close()
            conn.close()
        except: pass

inicializar_banco()

# 2. CONTROLE DE TEMA E SESSÃO
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'tema_atual' not in st.session_state: st.session_state['tema_atual'] = st.get_option("theme.base")

# Se o tema mudar, força o Rerun
if st.session_state['tema_atual'] != st.get_option("theme.base"):
    st.session_state['tema_atual'] = st.get_option("theme.base")
    st.rerun()

# 3. TELA DE LOGIN
if not st.session_state['logado']:
    # Logo
    tema = st.session_state['tema_atual']
    caminho_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "logo_escuro.png" if tema == "dark" else "logo_claro.png")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists(caminho_logo): st.image(caminho_logo, use_container_width=True)
    
    st.markdown("<h2 style='text-align: center;'>🐾 AuQMiaSis</h2>", unsafe_allow_html=True)

    # JavaScript para Foco e Enter
    components.html("""
    <script>
        // Foco inicial
        setTimeout(function() {
            var inputs = window.parent.document.querySelectorAll('input');
            if (inputs.length > 0) inputs[0].focus();
        }, 800);

        // Navegação com Enter bloqueando o submit automático
        window.parent.document.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                var inputs = Array.from(window.parent.document.querySelectorAll('input'));
                var index = inputs.indexOf(document.activeElement);
                if (index > -1 && index < inputs.length - 1) {
                    e.preventDefault();
                    e.stopImmediatePropagation();
                    inputs[index + 1].focus();
                }
            }
        }, true);
    </script>
    """, height=0)

    # Login Container (Sem form para evitar auto-submit)
    usuario_input = st.text_input("Usuário", key="campo1")
    senha_input = st.text_input("Senha", type="password", key="campo2")
    
    if st.button("Entrar no Sistema", use_container_width=True):
        conn = obter_conexao()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nivel FROM usuarios WHERE usuario = %s AND senha = %s", (usuario_input, senha_input))
            resultado = cursor.fetchone()
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
    if st.sidebar.button("Sair"):
        st.session_state['logado'] = False
        st.rerun()
        
    if menu_opcao == "Início / Painel": st.title("🐾 Painel Principal")
    elif menu_opcao == "Usuários": tela_usuarios()
    elif menu_opcao == "Clientes e Pets": tela_clientes()