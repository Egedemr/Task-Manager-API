# Milestone 4 — Filters + Pagination + Postman Examples ✅

## Implemented Features

### Task Filters
The `GET /tasks` endpoint now supports:
- `status` (todo, in_progress, done)
- `priority` (low, medium, high)
- `due_before` (ISO 8601 datetime)

### Sorting
- `sort` by: `id`, `title`, `status`, `priority`, `due_date`
- Prefix with `-` for descending order (e.g., `-due_date`)

### Pagination
- `limit` (default: 20, max: 100)
- `offset` (default: 0)

## Examples

- Filter by status and limit:
  - `GET /tasks?status=done&limit=10`

- Filter by priority and due date, sorted by due date (desc):
  - `GET /tasks?priority=high&due_before=2026-12-31T23:59:59Z&sort=-due_date&limit=5&offset=0`

- Pagination only:
  - `GET /tasks?limit=2&offset=0`

## Postman Collection Updates

Added ready‑to‑run examples under **Tasks** folder in:
- `Task_Manager_API.postman_collection.json`

Examples included:
- `status=done&limit=10`
- `priority=high&due_before=...&sort=-due_date&limit=5&offset=0`

## Done When

✅ Filter and pagination behavior verified from Postman.
