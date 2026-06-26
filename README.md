# PlayBook — Backend

Trabalho da disciplina de Programação para Web (PUC-Rio, 2026/1).

**Integrantes:** 
Breno Raisch - 2110039
João Pedro Paiva - 211xxxx

PlayBook é uma plataforma para jogadores de CS2 catalogarem e organizarem estratégias de jogo (execuções, defesas, anti-ecos, etc). O backend expõe uma API REST construída com Django + Django REST Framework, com autenticação via JWT e documentação Swagger.

## Stack

- Django 4.2 + Django REST Framework
- Autenticação JWT (`djangorestframework-simplejwt`)
- Documentação OpenAPI/Swagger (`drf-spectacular`)
- Banco de dados SQLite (desenvolvimento)

## Instalação local

```bash
git clone <url-deste-repositorio>
cd playbook-backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

A API fica disponível em `http://127.0.0.1:8000/`.

### Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste se necessário (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`).

## Rodando com Docker

```bash
docker build -t playbook-backend .
docker run --rm -p 8000:8000 --env-file .env playbook-backend
```

O container roda as migrations automaticamente antes de subir o servidor (Gunicorn) em `http://localhost:8000/`.

## Documentação da API (Swagger)

Com o servidor rodando, acesse:

- **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
- **Schema OpenAPI (JSON):** `http://127.0.0.1:8000/api/schema/`

## Endpoints principais

### Autenticação (`/api/auth/`)

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| POST | `/api/auth/register/` | Cria um novo usuário | Não |
| POST | `/api/auth/login/` | Login, retorna tokens JWT (access/refresh) | Não |
| POST | `/api/auth/logout/` | Invalida o refresh token | Sim |
| POST | `/api/auth/token/refresh/` | Renova o access token | Não |
| POST | `/api/auth/password/change/` | Troca de senha do usuário logado | Sim |
| POST | `/api/auth/password/reset/` | Solicita recuperação de senha | Não |
| POST | `/api/auth/password/reset/confirm/` | Confirma nova senha via token | Não |

### Plays (`/api/plays/`)

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| GET | `/api/plays/` | Lista plays públicas (filtros: `map`, `players_required`, granadas) | Sim |
| POST | `/api/plays/` | Cria uma play | Sim |
| GET | `/api/plays/{id}/` | Detalhe de uma play | Sim |
| PUT/PATCH | `/api/plays/{id}/` | Edita uma play (só autor) | Sim |
| DELETE | `/api/plays/{id}/` | Remove uma play (só autor) | Sim |
| GET | `/api/plays/my/` | Plays do usuário logado (públicas e privadas) | Sim |

### Playbooks (`/api/playbooks/`)

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| GET | `/api/playbooks/` | Lista playbooks públicos | Sim |
| POST | `/api/playbooks/` | Cria um playbook | Sim |
| GET | `/api/playbooks/{id}/` | Detalhe de um playbook | Sim |
| PUT/PATCH | `/api/playbooks/{id}/` | Edita um playbook (só autor) | Sim |
| DELETE | `/api/playbooks/{id}/` | Remove um playbook (só autor) | Sim |
| GET | `/api/playbooks/my/` | Playbooks do usuário logado (públicos e privados) | Sim |
| POST | `/api/playbooks/{id}/plays/add/` | Adiciona uma play ao playbook | Sim |
| POST | `/api/playbooks/{id}/plays/remove/` | Remove uma play do playbook | Sim |

## Regras de visibilidade

- Usuário não autenticado não acessa nenhum dado da API (exceto registro/login).
- Usuário autenticado vê todas as Plays/Playbooks **públicos** de qualquer autor, e todos os seus próprios (públicos ou privados).
- Apenas o autor pode editar ou excluir suas Plays e Playbooks (`IsAuthorOrReadOnly`).
- Uma Play privada de outro usuário não pode ser adicionada a um Playbook.

## Manual de uso (resumo)

1. Registre um usuário em `/api/auth/register/` (ou faça login se já tiver conta).
2. Use o `access` token retornado no header `Authorization: Bearer <token>` nas próximas requisições.
3. Crie Plays em `/api/plays/` informando mapa, granadas necessárias, vídeo, etc.
4. Agrupe Plays em um Playbook via `/api/playbooks/`, usando `plays/add` e `plays/remove` para gerenciar quais Plays pertencem a ele.
5. Marque `visibility` como `public` para que outros usuários autenticados vejam suas Plays/Playbooks.
