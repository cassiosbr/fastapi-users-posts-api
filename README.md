# FastAPI User API

Este projeto é uma API de usuários construída com FastAPI, seguindo boas práticas de arquitetura e separação de responsabilidades.

## Padrões Utilizados

### 1. Camadas do Projeto

- **Rotas (routes):** Responsáveis por receber as requisições HTTP e retornar respostas. Não possuem lógica de negócio.
- **Serviços (services):** Contêm a lógica de negócio e validações. Orquestram as operações entre rotas e repositórios.
- **Repositórios (repositories):** Responsáveis por interagir diretamente com o banco de dados (CRUD).
- **Modelos (models):** Definem as entidades do banco de dados usando SQLAlchemy.
- **Schemas:** Definem os contratos de entrada e saída da API usando Pydantic.
- **Core:** Configurações e utilitários centrais do projeto.

### 2. Autenticação

- Utiliza OAuth2 com JWT para autenticação.
- Endpoint de login: `/auth/login` (POST, recebe `username` e `password` via form).
- O token JWT é retornado no formato `{ "access_token": ..., "token_type": "bearer" }`.

### 3. Testes

- Testes unitários utilizam mocks para isolar dependências.
- Testes de serviços validam regras de negócio e integração entre camadas.

### 4. Boas Práticas

- Separação clara de responsabilidades entre camadas.
- Validações e regras de negócio centralizadas na camada de serviço.
- Repositórios apenas com operações de banco de dados.
- Uso de tipagem e Pydantic para validação de dados.

## Como Rodar o Projeto

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute a aplicação:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

## Como Rodar os Testes

```bash
pytest -v
```

## Estrutura de Pastas

```
app/
  api/           # Rotas e dependências
  core/          # Configurações e utilitários
  db/            # Sessão e conexão com o banco
  models/        # Modelos SQLAlchemy
  repositories/  # Repositórios (CRUD)
  schemas/       # Schemas Pydantic
  services/      # Lógica de negócio
```