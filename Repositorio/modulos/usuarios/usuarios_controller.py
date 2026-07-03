"""
Autor: Angelo Francisco da Silva
Data: 02/07/2026
Projeto: AuQMiaSis
"""

import sys
import os
# Garante o mapeamento correto das pastas DTOs e Models que estão na raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pydantic import ValidationError
from dtos.usuarios_dto import UsuarioCadastroDTO, UsuarioResponseDTO
from models.usuarios_model import UsuariosModel

class UsuariosController:
    """
    Controller responsável por intermediar o fluxo de dados entre a View (interface),
    o DTO (validação) e o Model (banco de dados).
    """

    @staticmethod
    def obter_todos_usuarios() -> list[UsuarioResponseDTO]:
        """Solicita ao Model a lista de usuários cadastrados."""
        return UsuariosModel.listar_todos()

    @staticmethod
    def cadastrar_novo_usuario(usuario_nome: str, senha_texto: str, nivel_acesso: str) -> dict:
        """
        Gerencia o fluxo de cadastro.
        Retorna um dicionário indicando o sucesso ou a mensagem de erro específica.
        """
        if not usuario_nome.strip() or not senha_texto.strip():
            return {"sucesso": False, "mensagem": "Todos os campos são obrigatórios!"}

        try:
            # 1. Valida as regras de negócio através do DTO
            dto = UsuarioCadastroDTO(usuario=usuario_nome, senha=senha_texto, nivel=nivel_acesso)
            
            # 2. Envia os dados limpos do DTO para persistência no banco
            if UsuariosModel.salvar(dto):
                return {"sucesso": True, "mensagem": f"Usuário '{dto.usuario}' cadastrado com sucesso!"}
            else:
                return {"sucesso": False, "mensagem": "Este nome de usuário já existe no sistema."}

        except ValidationError as e:
            # Captura erros de validação do Pydantic (ex: espaços em branco ou tamanho mínimo)
            mensagens_erro = [erro['msg'] for erro in e.errors()]
            return {"sucesso": False, "mensagem": mensagens_erro[0]}

    @staticmethod
    def remover_usuario(id_usuario: int) -> bool:
        """Comanda a exclusão de um usuário no banco de dados através do Model."""
        return UsuariosModel.deletar(id_usuario)