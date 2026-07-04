"""
Autor: Angelo Francisco da Silva
Data: 03/07/2026
Projeto: AuQMiaSis
"""
from database_config import obter_conexao

def inserir_cliente(cliente_dto):
    conn = obter_conexao()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, apelido, telefone, endereco, usa_frete, valor_frete)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (cliente_dto.nome, cliente_dto.apelido, cliente_dto.telefone, cliente_dto.endereco, cliente_dto.usa_frete, cliente_dto.valor_frete))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except:
        return False

def listar_clientes():
    conn = obter_conexao()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return clientes