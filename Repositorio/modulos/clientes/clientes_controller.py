"""
Autor: Angelo Francisco da Silva
Data: 03/07/2026
Projeto: AuQMiaSis
"""
from ...dtos.clientes_dto import ClienteDTO
from ...models.clientes_model import inserir_cliente, listar_clientes

def adicionar_novo_cliente(dados):
    try:
        cliente = ClienteDTO(**dados)
        if inserir_cliente(cliente):
            return {"sucesso": True, "mensagem": "Cliente cadastrado com sucesso!"}
        return {"sucesso": False, "mensagem": "Erro ao salvar no banco."}
    except Exception as e:
        return {"sucesso": False, "mensagem": str(e)}

def obter_todos_clientes():
    return listar_clientes()