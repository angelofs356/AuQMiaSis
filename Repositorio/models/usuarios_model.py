"""
Autor: Angelo Francisco da Silva
Data: 02/07/2026
Projeto: AuQMiaSis
"""

import sys
import os
# Adiciona automaticamente a raiz do projeto ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import psycopg2
from psycopg2 import extras
from database_config import obter_conexao
from dtos.usuarios_dto import UsuarioCadastroDTO, UsuarioResponseDTO

class UsuariosModel:
    """
    Model encarregado de executar todas as operações de banco de dados (SQL)
    referentes à tabela de usuários, utilizando DTOs para entrada e saída de dados.
    """

    @staticmethod
    def listar_todos() -> list[UsuarioResponseDTO]:
        """Busca todos os usuários cadastrados e os retorna mapeados em DTOs."""
        conn = obter_conexao()
        if not conn:
            return []
        try:
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute("SELECT id, usuario, nivel FROM usuarios ORDER BY usuario ASC")
            linhas = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return [UsuarioResponseDTO(**linha) for linha in linhas]
        except Exception:
            if conn:
                conn.close()
            return []

    @staticmethod
    def salvar(dto: UsuarioCadastroDTO) -> bool:
        """Insere um novo usuário no banco de dados com base nos dados validados do DTO."""
        conn = obter_conexao()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (dto.usuario,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return False
            
            cursor.execute(
                "INSERT INTO usuarios (usuario, senha, nivel) VALUES (%s, %s, %s)",
                (dto.usuario, dto.senha, dto.nivel)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception:
            if conn:
                conn.close()
            return False

    @staticmethod
    def deletar(id_usuario: int) -> bool:
        """Remove um usuário do banco através do seu ID identificador."""
        conn = obter_conexao()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception:
            if conn:
                conn.close()
            return False