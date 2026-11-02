# API de Gerenciamento de Clientes

API REST desenvolvida em Python com FastAPI e SQL Server, com operações CRUD (criar, consultar, atualizar e excluir clientes).

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQL Server
- PyODBC
- Pydantic
- Pytest

## Funcionalidades

- Listar clientes
- Buscar cliente por ID
- Cadastrar clientes
- Atualizar dados de clientes
- Excluir clientes
- Validar a existência de pedidos antes de excluir um cliente

## Estrutura do projeto

```text
projeto-api-banco-docker/
├── app/
│   ├── main.py
│   └── database.py
├── tests/
│   └── test_main.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Configuração e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/stefanidev/projeto-api-banco-docker.git
cd projeto-api-banco-docker
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
```

Ativar no Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto, seguindo o modelo `.env.example`.

Configure os dados de conexão com o SQL Server:

```env
SERVER=SEU_SERVIDOR
DATABASE=SEU_BANCO
DRIVER=ODBC Driver 18 for SQL Server
```

É necessário ter o SQL Server e o driver ODBC compatíveis instalados.

### 5. Executar a API

```bash
uvicorn app.main:app --reload
```

A documentação interativa estará disponível em:

http://127.0.0.1:8000/docs

## Executar os testes

```bash
python -m pytest -v
```
