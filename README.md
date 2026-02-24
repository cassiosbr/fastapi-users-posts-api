# FastAPI Users + Posts API

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

## Endpoints

Observação: as rotas de `users` e `posts` usam autenticação via Bearer Token.

### Auth

- `POST /auth/login`
   - Body (form): `username=<email>` e `password=<senha>`
   - Response: `{ "access_token": "...", "token_type": "bearer" }`

Exemplo (cURL):

```bash
curl -X POST "http://localhost:8000/auth/login" \
   -H "Content-Type: application/x-www-form-urlencoded" \
   -d "username=seu@email.com&password=sua_senha"
```

Use o token nas demais rotas:

```bash
export TOKEN="<seu_access_token>"
```

### Users

- `POST /users/` cria usuário
- `GET /users/` lista usuários (sem posts)
- `GET /users/{user_id}` busca usuário por id

### Posts

- `POST /posts/` cria post para o usuário autenticado
   - Body (JSON):
      - `title`: string
      - `content`: string
- `GET /posts/` lista todos os posts

Exemplo (cURL) criar post:

```bash
curl -X POST "http://localhost:8000/posts/" \
   -H "Authorization: Bearer $TOKEN" \
   -H "Content-Type: application/json" \
   -d '{"title":"Meu post","content":"Conteúdo do post"}'
```

Exemplo (cURL) listar posts:

```bash
curl -X GET "http://localhost:8000/posts/" \
   -H "Authorization: Bearer $TOKEN"
```

## Lazy loading (carregamento de posts)

Para evitar retornar posts desnecessariamente em listagens comuns, a API separa:

- `GET /users/`: retorna apenas dados do usuário (mais leve)
- `GET /users-posts`: retorna usuários + seus posts (quando você realmente precisa)

Implementação:

- A relação `User.posts` é uma relationship do SQLAlchemy e, por padrão, só carrega os posts quando acessada (lazy loading do ORM).
- No endpoint que retorna usuários **com** posts, a query usa `selectinload(User.posts)` para buscar os posts de forma eficiente e evitar o problema N+1.

Exemplo (cURL) listar usuários com posts:

```bash
curl -X GET "http://localhost:8000/users-posts" \
   -H "Authorization: Bearer $TOKEN"
```

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