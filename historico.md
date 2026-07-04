🐾 DOCUMENTO DE CONTEXTO TÉCNICO E MEMÓRIA DE PROJETO: AuQMiaSis
Autor do Projeto: Angelo Francisco da Silva

Data do Último Marco: 03/07/2026

Nome do Projeto: AuQMiaSis (Sistema de Gerenciamento de Banho e Tosa)

Objetivo: Backup de Contexto Absoluto para inicialização e leitura de IA (LLM).

🛠️ 1. ESPECIFICAÇÕES TECNOLÓGICAS, FERRAMENTAS E VERSÕES
Linguagem Core: Python 3.12 (Versão: 3.12.10).

Framework (Front-end): Streamlit.

Banco de Dados: PostgreSQL (Hospedado na nuvem via Aiven).

Provedor de Conexão SQL: psycopg2.

Validação de Dados: Pydantic v2.

Framework de Testes: Pytest.

🔑 2. INFRAESTRUTURA E CONEXÃO ATUAL (AIVEN)
Host: pg-1e753199-auqmiasis.c.aivencloud.com

Porta: 19111

Banco: defaultdb

Usuário: avnadmin

Regra de Conexão: A conexão agora é centralizada via string de conexão única (URL) no arquivo .streamlit/secrets.toml, lida pelo database_config.py através da função obter_conexao().

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

📝 5. PADRÕES ESTRUTURAIS E ARQUITETURA DE DESENVOLVIMENTO
Padronização de Cabeçalhos: Todos os arquivos .py devem conter obrigatoriamente a docstring de identificação:

Python
"""
Autor: Angelo Francisco da Silva
Data: [DD/MM/AAAA]
Projeto: AuQMiaSis
"""
Arquitetura em Camadas (MVC + DTO):

View (*_view.py): Responsável estrita pela interface Streamlit. Captura entradas e exibe resultados. Não interage diretamente com o banco de dados ou schemas.

Controller (*_controller.py): Camada de orquestração. Valida dados via DTO, aciona a lógica do Model e padroniza respostas para a View no formato {"sucesso": bool, "mensagem": str}.

DTO (*_dto.py): Schemas Pydantic para garantir a integridade, tipagem e higienização dos dados antes da persistência.

Model (*_model.py): Camada de persistência. Executa comandos SQL puros e gerencia a interface com o banco de dados via psycopg2.

🎯 6. ESTADO ATUAL DO SISTEMA E PRÓXIMO PASSO

Infraestrutura e Conectividade:

Componentes Prontos e Validados:
Inicialização: O app.py conecta no Aiven com segurança, valida ou cria as 10 tabelas e provê formulário de login funcional. Cria o usuário padrão (admin / admin123) caso a tabela esteja vazia.

Centralização de Conexão: A lógica de conexão foi refatorada para o módulo database_config.py. Toda a aplicação utiliza agora a função obter_conexao(), que lê uma única string de conexão (url) a partir do secrets.toml.

Segurança: Credenciais sensíveis são protegidas pelo .gitignore e não existem mais strings de conexão "hardcoded" ou montadas manualmente nos arquivos de lógica (app.py), eliminando riscos de vazamento e erros de DNS.

Componentes Validados:

Sistema Maestro (app.py): Fluxo de inicialização do banco (criação das 10 tabelas), login e controle de sessão validados.

Módulo de Usuários: CRUD completo funcional (View, Controller, DTO, Model) e coberto por 4 testes unitários (pytest) com 100% de sucesso.

Próxima Sprint (Roadmap):

Módulo de Clientes e Pets: Iniciar a implementação replicando o padrão MVC+DTO e os protocolos de segurança estabelecidos. A suíte de testes deve ser expandida para cobrir as novas regras de negócio deste módulo.

Módulo de Usuários: Camadas DTO, Model, Controller e View totalmente criadas, integradas e acopladas ao menu do arquivo maestro.

Qualidade e Testes: O arquivo pytest.ini na raiz parametriza o pythonpath = Repositorio. Há 4 testes unitários cobrindo o comportamento do Pydantic e do fluxo do controller no arquivo test_usuarios.py. Todos os 4 testes passam com sucesso (green session) rodando o comando pytest a partir da pasta E:\AuQMiaSis.

Ponto de Parada Exato (Próxima Sprint/Tarefa):
O ambiente de desenvolvimento está estável e funcional em execução local via comando streamlit run Repositorio/app.py. O próximo passo do desenvolvimento consiste em iniciar o Módulo de Cadastro e Consulta de Clientes e Pets, replicando estritamente os padrões modulares, de cabeçalho, arquitetura em camadas e suíte de testes estabelecidos no módulo de usuários.

📝 Resumo das Alterações (04/07/2026)
Progresso no Sistema "AuQMiaSis":

Refatoração do Sistema de Login e Navegação (app.py):

Implementação de Logo Dinâmica: Adicionada a função exibir_logo() que detecta automaticamente o tema do Streamlit (light ou dark) e carrega o arquivo de imagem correspondente (logo_claro.png ou logo_escuro.png) da pasta img/. A lógica foi protegida com st.empty() e um controle de estado (st.session_state['tema_atual']) para forçar a atualização instantânea da interface ao trocar de tema.

Otimização do Fluxo de Login (Foco e "Enter"): Substituímos a estrutura rígida de st.form por um st.container para obter controle total sobre os eventos do navegador. Injetamos um script JavaScript via st.components.v1.html que:

Define o foco inicial automaticamente no primeiro campo (Usuário).

Intercepta a tecla Enter em campos de texto para navegar para o próximo campo (tabIndex), bloqueando o submit automático e permitindo o envio apenas através do clique explícito no botão "Entrar".

Correção de Erros de Caminho: Ajustamos o carregamento de arquivos estáticos utilizando os.path.abspath(__file__) para garantir que o sistema encontre a logo e outros recursos independentemente de onde o terminal seja aberto.

Estrutura de Módulos:

Validada a estrutura de pacotes com __init__.py em todas as subpastas.

Corrigida a importação de módulos para o formato absoluto (from modulos.clientes... em vez de importações relativas), resolvendo o erro ImportError: attempted relative import beyond top-level package que ocorria ao executar o sistema via python -m streamlit.

Ambiente de Desenvolvimento:

O sistema continua rodando estavelmente a partir da raiz E:\AuQMiaSis com o comando python -m streamlit run Repositorio/app.py.

Próximo Passo (Sprint: Módulo de Clientes e Pets):

O ambiente está configurado e as ferramentas de UI (foco/logo/navegação) estão padronizadas.

Tarefa imediata para a próxima sessão: Iniciar a criação efetiva dos arquivos clientes_dto.py, clientes_model.py, clientes_controller.py e clientes_view.py, seguindo rigorosamente o cabeçalho e a arquitetura MVC+DTO estabelecidos no historico.md.

Dica para amanhã: Ao retomar, você já pode começar criando a estrutura da pasta Repositorio/modulos/clientes/ com os arquivos que esboçamos. O sistema está pronto para receber essa nova funcionalidade sem conflitos!