# Task Manager API

FastAPI-based Task Manager API with JWT authentication, task CRUD, filtering, sorting, pagination, and tests.

## Features

- JWT auth (signup, login, current user)
- Task CRUD (create, list, get, update, delete)
- Filters: status, priority, due_before
- Sorting: `sort=id|title|status|priority|due_date` (prefix with `-` for desc)
- Pagination: `limit`, `offset`
- Postman collection + environment
- Pytest coverage for auth, CRUD, ownership, filters

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Update `DATABASE_URL` in `.env`.
Do not commit `.env` (it contains local secrets).

## Run

```bash
uvicorn app.main:app --reload
```

Open API docs:
- http://localhost:8000/docs

## Example curl requests

### Signup
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"YOUR_PASSWORD"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=YOUR_PASSWORD"
```

### Create task
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Task","status":"todo","priority":"medium"}'
```

### List tasks with filters
```bash
curl "http://localhost:8000/tasks?status=done&limit=10" \
  -H "Authorization: Bearer <TOKEN>"
```

### Sorting and pagination
```bash
curl "http://localhost:8000/tasks?sort=-due_date&limit=5&offset=0" \
  -H "Authorization: Bearer <TOKEN>"
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Postman

Collection: [postman/Task_Manager_API.postman_collection.json](postman/Task_Manager_API.postman_collection.json)

Environment (optional): [postman/Task_Manager_API.postman_environment.json](postman/Task_Manager_API.postman_environment.json)

Import both into Postman, then run **Auth → Login** to auto‑set `{{access_token}}` and test other requests.
