"""
Autor: Angelo Francisco da Silva
Data: 02/07/2026
Projeto: AuQMiaSis
"""

from pydantic import BaseModel, Field, field_validator

class UsuarioCadastroDTO(BaseModel):
    """
    DTO responsável por capturar e validar os dados vindos do formulário
    de cadastro antes de enviar para o banco de dados.
    """
    usuario: str = Field(..., min_length=3, max_length=50)
    senha: str = Field(..., min_length=4)
    nivel: str

    @field_validator('usuario')
    @classmethod
    def validar_usuario_sem_espacos(cls, v: str) -> str:
        """Garante que o nome de login não tenha espaços e seja sempre minúsculo."""
        if " " in v:
            raise ValueError("O nome de usuário não pode conter espaços em branco.")
        return v.lower().strip()

class UsuarioResponseDTO(BaseModel):
    """
    DTO utilizado para transportar os dados dos usuários vindos do banco
    com segurança para serem exibidos na tela.
    """
    id: int
    usuario: str
    nivel: str