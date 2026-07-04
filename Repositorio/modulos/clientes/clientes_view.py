"""
Autor: Angelo Francisco da Silva
Data: 03/07/2026
Projeto: AuQMiaSis
"""
import streamlit as st
from .clientes_controller import adicionar_novo_cliente, obter_todos_clientes

def tela_clientes():
    st.title("🐾 Cadastro de Clientes")
    tab1, tab2 = st.tabs(["🔍 Consultar", "➕ Cadastrar"])

    with tab2:
        with st.form("form_cliente"):
            nome = st.text_input("Nome Completo")
            apelido = st.text_input("Apelido")
            telefone = st.text_input("Telefone")
            endereco = st.text_input("Endereço")
            usa_frete = st.selectbox("Usa Frete?", ["Sim", "Não"])
            valor_frete = st.number_input("Valor Frete", value=0.0)
            
            if st.form_submit_button("Salvar"):
                dados = {"nome": nome, "apelido": apelido, "telefone": telefone, 
                         "endereco": endereco, "usa_frete": usa_frete, "valor_frete": valor_frete}
                resultado = adicionar_novo_cliente(dados)
                if resultado["sucesso"]:
                    st.success(resultado["mensagem"])
                else:
                    st.error(resultado["mensagem"])

    with tab1:
        st.write(obter_todos_clientes())