"""
Autor: Angelo Francisco da Silva
Data: 02/07/2026
Projeto: AuQMiaSis
"""

import streamlit as st
from modulos.usuarios.usuarios_controller import UsuariosController

def tela_usuarios():
    st.title("👤 Gerenciamento de Usuários")
    st.markdown("Cadastre novos operadores ou gerencie as contas que acessam o sistema.")
    
    # Criando abas para organizar a tela de forma elegante
    aba_consulta, aba_cadastro = st.tabs(["🔍 Consultar e Gerenciar", "➕ Cadastrar Novo"])
    
    # --- ABA: CADASTRAR NOVO ---
    with aba_cadastro:
        st.subheader("Novo Usuário")
        with st.form("form_cadastro_usuario", clear_on_submit=True):
            novo_nome = st.text_input("Nome de Usuário (Login)", placeholder="Ex: angelo.admin")
            nova_senha = st.text_input("Senha", type="password", placeholder="No mínimo 4 caracteres")
            novo_nivel = st.selectbox("Nível de Acesso", ["Administrador", "Atendente", "Tosador"])
            
            botao_salvar = st.form_submit_button("💾 Salvar Usuário")
            
            if botao_salvar:
                # O Controller processa os dados, valida via DTO e tenta salvar
                retorno = UsuariosController.cadastrar_novo_usuario(
                    usuario_nome=novo_nome, 
                    senha_texto=nova_senha, 
                    nivel_acesso=novo_nivel
                )
                
                if retorno["sucesso"]:
                    st.success(retorno["mensagem"])
                    st.rerun()
                else:
                    st.error(retorno["mensagem"])

    # --- ABA: CONSULTAR E GERENCIAR ---
    with aba_consulta:
        st.subheader("Usuários Ativos")
        
        # Pede a lista de usuários formatada pelo DTO de Resposta via Controller
        usuarios = UsuariosController.obter_todos_usuarios()
        
        if not usuarios:
            st.info("Nenhum usuário cadastrado no sistema.")
        else:
            # Renderiza os cabeçalhos das colunas
            col_user, col_nivel, col_acao = st.columns([2, 2, 1])
            col_user.markdown("**Usuário**")
            col_nivel.markdown("**Nível de Acesso**")
            col_acao.markdown("**Ações**")
            st.markdown("---")
            
            # Lista cada usuário com um botão de exclusão
            for u in usuarios:
                col1, col2, col3 = st.columns([2, 2, 1])
                col1.write(f"{u.usuario}")
                col2.write(f"`{u.nivel}`")
                
                with col3:
                    # Proteção para não deletar o administrador padrão do sistema
                    if u.usuario == 'admin':
                        st.write("🔒 Protegido")
                    else:
                        # Chave única para o botão usando o ID do banco de dados
                        if st.button("❌ Excluir", key=f"del_{u.id}"):
                            if UsuariosController.remover_usuario(u.id):
                                st.success("Usuário removido com sucesso!")
                                st.rerun()
                            else:
                                st.error("Erro ao tentar remover o usuário.")