"""
Autor: Angelo Francisco da Silva
Data: 03/07/2026
Projeto: AuQMiaSis
"""
import pytest
from dtos.clientes_dto import ClienteDTO
from pydantic import ValidationError

def test_cliente_dto_valido():
    """Testa se o DTO aceita dados corretos."""
    dados = {
        "nome": "João Silva",
        "apelido": "João",
        "telefone": "999999999",
        "endereco": "Rua A, 100",
        "usa_frete": "Sim",
        "valor_frete": 15.0
    }
    cliente = ClienteDTO(**dados)
    assert cliente.nome == "João Silva"
    assert cliente.valor_frete == 15.0

def test_cliente_dto_nome_invalido():
    """Testa se o DTO falha com nome muito curto (menos de 2 caracteres)."""
    dados = {
        "nome": "J",
        "apelido": "J",
        "telefone": "9999",
        "endereco": "Rua B",
        "usa_frete": "Não",
        "valor_frete": 0.0
    }
    with pytest.raises(ValidationError):
        ClienteDTO(**dados)

def test_cliente_dto_tipagem_frete():
    """Testa se o DTO converte corretamente o tipo do valor_frete."""
    dados = {
        "nome": "Maria",
        "apelido": "Mary",
        "telefone": "8888",
        "endereco": "Rua C",
        "usa_frete": "Sim",
        "valor_frete": "20.5" # Enviando como string, o Pydantic deve converter para float
    }
    cliente = ClienteDTO(**dados)
    assert isinstance(cliente.valor_frete, float)
    assert cliente.valor_frete == 20.5