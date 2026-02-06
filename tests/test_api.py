import uuid
from datetime import datetime, timedelta


def signup(client, email: str, password: str = "testpass123"):
    return client.post(
        "/auth/signup",
        json={"email": email, "password": password},
    )


def login(client, email: str, password: str = "testpass123"):
    return client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def auth_header(token: str):
    return {"Authorization": f"Bearer {token}"}


def create_task(client, token: str, payload: dict):
    return client.post("/tasks", json=payload, headers=auth_header(token))


def unique_email() -> str:
    return f"user_{uuid.uuid4().hex[:8]}@example.com"


def test_auth_flow(client):
    email = unique_email()
    resp = signup(client, email)
    assert resp.status_code == 201

    resp = login(client, email)
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data


def test_create_and_list_tasks(client):
    email = unique_email()
    signup(client, email)
    token = login(client, email).json()["access_token"]

    task_payload = {"title": "My Task", "status": "todo", "priority": "medium"}
    create_resp = create_task(client, token, task_payload)
    assert create_resp.status_code == 201

    list_resp = client.get("/tasks", headers=auth_header(token))
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1


def test_get_task_by_id(client):
    email = unique_email()
    signup(client, email)
    token = login(client, email).json()["access_token"]

    create_resp = create_task(
        client,
        token,
        {"title": "Get Task", "status": "todo", "priority": "low"},
    )
    task_id = create_resp.json()["id"]

    get_resp = client.get(f"/tasks/{task_id}", headers=auth_header(token))
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == task_id


def test_update_task(client):
    email = unique_email()
    signup(client, email)
    token = login(client, email).json()["access_token"]

    create_resp = create_task(
        client,
        token,
        {"title": "Update Task", "status": "todo", "priority": "low"},
    )
    task_id = create_resp.json()["id"]

    update_resp = client.patch(
        f"/tasks/{task_id}",
        json={"status": "in_progress", "priority": "high"},
        headers=auth_header(token),
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "in_progress"
    assert update_resp.json()["priority"] == "high"


def test_delete_task(client):
    email = unique_email()
    signup(client, email)
    token = login(client, email).json()["access_token"]

    create_resp = create_task(
        client,
        token,
        {"title": "Delete Task", "status": "todo", "priority": "low"},
    )
    task_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/tasks/{task_id}", headers=auth_header(token))
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/tasks/{task_id}", headers=auth_header(token))
    assert get_resp.status_code == 404


def test_task_ownership(client):
    email1 = unique_email()
    email2 = unique_email()
    signup(client, email1)
    signup(client, email2)

    token1 = login(client, email1).json()["access_token"]
    token2 = login(client, email2).json()["access_token"]

    create_resp = create_task(
        client,
        token1,
        {"title": "Owner Task", "status": "todo", "priority": "medium"},
    )
    task_id = create_resp.json()["id"]

    other_get = client.get(f"/tasks/{task_id}", headers=auth_header(token2))
    assert other_get.status_code == 404

    other_update = client.patch(
        f"/tasks/{task_id}",
        json={"status": "done"},
        headers=auth_header(token2),
    )
    assert other_update.status_code == 404

    other_delete = client.delete(f"/tasks/{task_id}", headers=auth_header(token2))
    assert other_delete.status_code == 404


def test_filtering_sorting_pagination(client):
    email = unique_email()
    signup(client, email)
    token = login(client, email).json()["access_token"]

    now = datetime.utcnow()
    tasks = [
        {"title": "T1", "status": "done", "priority": "high", "due_date": (now + timedelta(days=5)).isoformat() + "Z"},
        {"title": "T2", "status": "done", "priority": "low", "due_date": (now + timedelta(days=2)).isoformat() + "Z"},
        {"title": "T3", "status": "todo", "priority": "medium", "due_date": (now + timedelta(days=10)).isoformat() + "Z"},
        {"title": "T4", "status": "in_progress", "priority": "high", "due_date": (now + timedelta(days=1)).isoformat() + "Z"},
    ]

    for t in tasks:
        create_task(client, token, t)

    # Filter status=done
    resp = client.get("/tasks?status=done", headers=auth_header(token))
    assert resp.status_code == 200
    assert all(task["status"] == "done" for task in resp.json())

    # Filter priority=high
    resp = client.get("/tasks?priority=high", headers=auth_header(token))
    assert resp.status_code == 200
    assert all(task["priority"] == "high" for task in resp.json())

    # Due before
    due_before = (now + timedelta(days=3)).isoformat() + "Z"
    resp = client.get(f"/tasks?due_before={due_before}", headers=auth_header(token))
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # Sort desc
    resp = client.get("/tasks?sort=-due_date", headers=auth_header(token))
    assert resp.status_code == 200
    dates = [task["due_date"] for task in resp.json()]
    assert dates == sorted(dates, reverse=True)

    # Pagination
    resp = client.get("/tasks?limit=2&offset=0", headers=auth_header(token))
    assert resp.status_code == 200
    assert len(resp.json()) == 2
