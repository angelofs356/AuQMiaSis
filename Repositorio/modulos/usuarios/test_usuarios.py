"""
Autor: Angelo Francisco da Silva
Data: 02/07/2026
Projeto: AuQMiaSis
"""

import pytest
from unittest.mock import patch
from pydantic import ValidationError
from dtos.usuarios_dto import UsuarioCadastroDTO
from modulos.usuarios.usuarios_controller import UsuariosController

def test_dto_deve_rejeitar_usuario_com_espacos():
    """Garante que a regra do DTO barra espaços em branco no login."""
    with pytest.raises(ValidationError):
        UsuarioCadastroDTO(usuario="joao tosa", senha="1234", nivel="Tosador")

def test_dto_deve_converter_usuario_para_minusculo():
    """Garante que o DTO padroniza o login salvando sempre em letras minúsculas."""
    dto = UsuarioCadastroDTO(usuario="AngeloAdmin", senha="1234", nivel="Administrador")
    assert dto.usuario == "angeloadmin"

@patch('models.usuarios_model.UsuariosModel.salvar')
def test_controller_deve_retornar_sucesso_ao_salvar_usuario_valido(mock_salvar):
    """Testa se o Controller processa corretamente o cadastro de um usuário válido."""
    mock_salvar.return_value = True
    resultado = UsuariosController.cadastrar_novo_usuario("marcos", "senha123", "Atendente")
    assert resultado["sucesso"] is True
    assert "cadastrado com sucesso" in resultado["mensagem"]

@patch('models.usuarios_model.UsuariosModel.salvar')
def test_controller_deve_rejeitar_campos_vazios(mock_salvar):
    """Garante que o Controller barra a operação se a senha ou usuário forem vazios."""
    resultado = UsuariosController.cadastrar_novo_usuario("   ", "1234", "Tosador")
    assert resultado["sucesso"] is False
    assert resultado["mensagem"] == "Todos os campos são obrigatórios!"
    mock_salvar.assert_not_called()