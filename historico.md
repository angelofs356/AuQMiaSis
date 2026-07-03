🐾 DOCUMENTO DE CONTEXTO TÉCNICO E MEMÓRIA DE PROJETO: AuQMiaSis
Plaintext
Autor do Projeto: Angelo Francisco da Silva
Data do Último Marco: 02/07/2026
Nome do Projeto: AuQMiaSis (Sistema de Gerenciamento de Banho e Tosa)
Objetivo: Backup de Contexto Absoluto para inicialização e leitura de IA (LLM).
🛠️ 1. ESPECIFICAÇÕES TECNOLÓGICAS, FERRAMENTAS E VERSÕES
Linguagem Core: Python 3.12 (Versão específica em uso: 3.12.10).

Framework de Interface (Front-end): Streamlit.

Banco de Dados: PostgreSQL (Hospedado na nuvem via Supabase).

Provedor de Conexão SQL: psycopg2 (com uso de psycopg2.extras.RealDictCursor).

Validação de Dados e Regras de Negócio: Pydantic v2 (Pydantic Core 2.13).

Framework de Testes Unitários: Pytest (Versão em uso: 9.1.1).

Ambiente de Desenvolvimento (IDE): VS Code (Visual Studio Code) utilizando o Workspace AuQMiaSis.code-workspace.

Gerenciador de Banco de Dados Local/Interface: DBeaver Community Edition (Site oficial: dbeaver.io).

🔑 2. INFORMAÇÕES DE INFRAESTRUTURA, SITES E CREDENCIAIS
Banco de Dados (Supabase)
Host/Endereço do Servidor: db.zpnxtrmbpnenuulidrwl.supabase.co

Porta padrão: 5432

Database (Banco): postgres

Username (Usuário): postgres

Password (Senha Pura): Feda40@14&12acada356

URL de Conexão JDBC (Para uso direto no DBeaver se necessário):
jdbc:postgresql://db.zpnxtrmbpnenuulidrwl.supabase.co:5432/postgres

Regras de Injeção de Credenciais no Código
A senha contém caracteres especiais (&). No código Python, ela é extraída estritamente do arquivo local e protegido .streamlit/secrets.toml.

Para evitar falhas no protocolo URI, a senha sofre obrigatoriamente mascaramento utilizando a função urllib.parse.quote_plus antes de compor a string de conexão final (DB_URI).

🗂️ 3. MAPEAMENTO COMPLETO DA ARQUITETURA DE DIRETÓRIOS
A estrutura atual do disco E:\ está organizada exatamente sob o seguinte mapa de pastas:

Plaintext
E:\AuQMiaSis>
│   AuQMiaSis.code-workspace
│   pytest.ini                       # Configuração do pythonpath para o Pytest
│   estrutura.txt                    # Log de estrutura do sistema
│   
├───.pytest_cache                    # Cache de testes da raiz
├───.vscode
│       settings.json                # Configurações de ambiente do VS Code
│       
├───Base
├───Documentação
│       Estrutura.docx
│       Guia de Configuração.docx
│       historico.md                 # Arquivo onde este texto está consolidado
│       
└───Repositorio                      # Raiz do código-fonte Python
    │   app.py                       # Arquivo Inicializador / Maestro do Sistema
    │   conftest.py                  # Configurações globais de fixtures do Pytest
    │   database_config.py           # Centralizador do Pool de Conexão com Supabase
    │   requirements.txt             # Dependências (pydantic, pytest, streamlit, psycopg2)
    │   
    ├───.pytest_cache                # Cache de testes do repositório
    ├───.streamlit
    │       secrets.toml             # Arquivo local com a senha do banco
    │       
    ├───dtos
    │       usuarios_dto.py          # Objetos de Transferência e Validação de Usuários
    │       __init__.py
    │       
    ├───models
    │       usuarios_model.py        # Camada de persistência/Queries SQL de Usuários
    │       __init__.py
    │       
    └───modulos
        └───usuarios
                test_usuarios.py       # Suite de 4 Testes Unitários (Pytest)
                usuarios_controller.py # Intermediário de Regras (View <-> DTO/Model)
                usuarios_view.py       # Interface Streamlit do CRUD de Usuários
                __init__.py
🗄️ 4. MODELAGEM DO BANCO DE DADOS (10 TABELAS DO ECOSSISTEMA)
O script contido no inicializador do banco cria automaticamente na nuvem a seguinte estrutura relacional:

usuarios: Controle de operadores. Campos: id (SERIAL PK), usuario (TEXT UNIQUE), senha (TEXT), nivel (TEXT).

clientes: Cadastro de tutores. Campos: id (SERIAL PK), nome (TEXT), apelido (TEXT), telefone (TEXT), endereco (TEXT), usa_frete (TEXT), valor_frete (REAL).

pets: Cadastro de animais vinculados a um cliente. Campos: id (SERIAL PK), cliente_id (INTEGER FK -> clientes), nome_pet (TEXT), classe (TEXT), raca (TEXT).

servicos: Catálogo de serviços. Campos: id (SERIAL PK), descricao (TEXT), valor (REAL), valor_pacote (REAL).

agendamentos: Agenda do Banho e Tosa. Campos: id (SERIAL PK), pet_id (INTEGER FK -> pets), servico_id (INTEGER FK -> servicos), data_hora (TEXT), status (TEXT).

fichas_entrada: Check-in do estado do pet. Campos: id (SERIAL PK), pet_id (INTEGER FK -> pets), condicao_geral (TEXT), data_registro (TEXT), foto (TEXT).

movimentacao: Fluxo financeiro por atendimento. Campos: id (SERIAL PK), pet_id (INTEGER), agendamento_id (INTEGER), servico_id (INTEGER), valor_servico (REAL), valor_frete (REAL), data_pagamento (TEXT), status_pagamento (TEXT).

financeiro_geral: Fluxo de caixa de despesas/receitas gerais. Campos: id (SERIAL PK), tipo (TEXT), descricao (TEXT), valor (REAL), data_vencimento (TEXT), status (TEXT).

pacotes_vendidos: Contratos de pacotes de serviços por cliente. Campos: id (SERIAL PK), cliente_id (INTEGER), nome_pacote (TEXT), valor_total (REAL), data_venda (TEXT).

itens_pacote: Controle de sessões dos pacotes. Campos: id (SERIAL PK), pacote_vendido_id (INTEGER), servico_id (INTEGER), qtd_total (INTEGER), qtd_usada (INTEGER).

📝 5. PADRÕES OBRIGATÓRIOS DE DESENVOLVIMENTO
Cabeçalho de Arquivo
Todo arquivo de script Python (.py) gerado no projeto deve, obrigatoriamente, iniciar com a seguinte estrutura de Docstring:

Python
"""
Autor: Angelo Francisco da Silva
Data: [Inserir data do dia]
Projeto: AuQMiaSis
"""
Arquitetura de Fluxo de Dados (Padrão MVC + DTO)
View (*_view.py): Captura as entradas brutas da interface Streamlit e renderiza os componentes visuais de resposta ao usuário. Proibido invocar o banco de dados ou schemas Pydantic direto na View. Ela consome apenas métodos do Controller. Organizada visualmente usando st.tabs dividida em: "🔍 Consultar e Gerenciar" e "➕ Cadastrar Novo".

Controller (*_controller.py): Intermediário lógico. Recebe os dados da View, repassa ao DTO correspondente para validação e aciona o Model. Captura exceções como ValidationError do Pydantic e as transforma em mensagens amigáveis retornando um dicionário padrão: {"sucesso": bool, "mensagem": str}.

DTO (*_dto.py): Schemas baseados em pydantic.BaseModel. Responsável pela limpeza, tipagem estrita e validação de regras de negócio antes de qualquer contato com o banco.

Model (*_model.py): Executa comandos SQL puras via conector, interagindo com as tabelas do Supabase. Recebe e retorna dados tipados via DTOs.

🎯 6. ESTADO ATUAL DO SISTEMA E PRÓXIMO PASSO
Componentes Prontos e Validados:
Inicialização: O app.py conecta no Supabase com segurança, valida ou cria as 10 tabelas e provê formulário de login funcional. Cria o usuário padrão (admin / admin123) caso a tabela esteja vazia.

Módulo de Usuários: Camadas DTO, Model, Controller e View totalmente criadas, integradas e acopladas ao menu do arquivo maestro.

Qualidade e Testes: O arquivo pytest.ini na raiz parametriza o pythonpath = Repositorio. Há 4 testes unitários cobrindo o comportamento do Pydantic e do fluxo do controller no arquivo test_usuarios.py. Todos os 4 testes passam com sucesso (green session) rodando o comando pytest a partir da pasta E:\AuQMiaSis.

Ponto de Parada Exato (Próxima Sprint/Tarefa):
O ambiente de desenvolvimento está estável e funcional em execução local via comando streamlit run Repositorio/app.py. O próximo passo do desenvolvimento consiste em iniciar o Módulo de Cadastro e Consulta de Clientes e Pets, replicando estritamente os padrões modulares, de cabeçalho, arquitetura em camadas e suíte de testes estabelecidos no módulo de usuários.