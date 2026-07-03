"""
Autor: Angelo Francisco da Silva
Data: 02/07/2026
Projeto: AuQMiaSis
"""

import sys
import os

# Força o Pytest a registrar a raiz do projeto no caminho de buscas do Python
raiz_projeto = os.path.abspath(os.path.dirname(__file__))
if raiz_projeto not in sys.path:
    sys.path.insert(0, raiz_projeto)