# Task Manager API - Milestone 3 Complete! ✅

## Implemented Features

### Protected Task Endpoints
All task endpoints require authentication (Bearer token):

- **POST /tasks** - Create a new task
- **GET /tasks** - Get all tasks for the authenticated user
- **GET /tasks/{id}** - Get a specific task by ID
- **PATCH /tasks/{id}** - Update a task (partial update)
- **DELETE /tasks/{id}** - Delete a task

### Task Schema
Tasks support the following fields:
- `title` (required, 1-200 characters)
- `description` (optional, max 1000 characters)
- `status` (todo, in_progress, done - default: todo)
- `priority` (low, medium, high - default: medium)
- `due_date` (optional, ISO 8601 datetime)

## Using the Postman Collection

### Import the Collection
1. Open Postman
2. Click **Import** button
3. Select the file: `Task_Manager_API.postman_collection.json`
4. The collection will appear with two folders: **Auth** and **Tasks**

### Collection Variables
The collection uses two variables:
- `{{base_url}}` - API base URL (default: http://localhost:8000)
- `{{access_token}}` - Automatically saved after login

### Testing Workflow
1. **Signup**: Create a new user account
   - Folder: Auth → Signup
   - Updates the email/password in the request body

2. **Login**: Get your access token
   - Folder: Auth → Login
   - The token is automatically saved to `{{access_token}}` variable
   - Use the same email/password from signup

3. **Create Task**: Add a new task
   - Folder: Tasks → Create Task
   - The task ID is automatically saved to `{{task_id}}` variable

4. **Get All Tasks**: View your tasks
   - Folder: Tasks → Get All Tasks

5. **Get Task by ID**: View a specific task
   - Folder: Tasks → Get Task by ID
   - Uses the saved `{{task_id}}`

6. **Update Task**: Modify a task
   - Folder: Tasks → Update Task
   - Partial updates supported (only send fields to change)

7. **Delete Task**: Remove a task
   - Folder: Tasks → Delete Task

### Alternative: Swagger UI
You can also test the API through Swagger UI:
- Navigate to: http://localhost:8000/docs
- Click **Authorize** button
- Enter: `Bearer YOUR_ACCESS_TOKEN`

## API Server
Make sure the server is running:
```bash
uvicorn app.main:app --reload
```

Server will be available at: http://127.0.0.1:8000

## Status Enums
- **Status**: `todo`, `in_progress`, `done`
- **Priority**: `low`, `medium`, `high`
