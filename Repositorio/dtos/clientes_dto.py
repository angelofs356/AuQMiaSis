"""
Autor: Angelo Francisco da Silva
Data: 03/07/2026
Projeto: AuQMiaSis
"""
from pydantic import BaseModel, Field

class ClienteDTO(BaseModel):
    nome: str = Field(..., min_length=2)
    apelido: str
    telefone: str
    endereco: str
    usa_frete: str
    valor_frete: float = 0.0