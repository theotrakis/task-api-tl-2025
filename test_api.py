import importlib
import pytest


@pytest.fixture()
def client(tmp_path, monkeypatch):
    # προσωρινό json για tests
    test_file = tmp_path / "tasks_test.json"
    test_file.write_text("[]", encoding="utf-8")

    # πες στο storage να χρησιμοποιήσει αυτό το αρχείο
    monkeypatch.setenv("TASKS_FILE", str(test_file))

    # reload modules ώστε να “πιάσουν” το env var
    import storage
    import app as app_module
    importlib.reload(storage)
    importlib.reload(app_module)

    return app_module.app.test_client()


def test_get_tasks_empty(client):
    res = client.get("/tasks")
    assert res.status_code == 200
    assert res.get_json() == []


def test_create_task_then_get_by_id(client):
    payload = {
        "username": "user1",
        "title": "Task 1",
        "description": "Desc",
        "deadline": "2026-01-31"
    }

    res_create = client.post("/tasks", json=payload)
    assert res_create.status_code in (200, 201)

    res_all = client.get("/tasks")
    tasks = res_all.get_json()
    assert isinstance(tasks, list)
    assert len(tasks) == 1

    task_id = tasks[0]["id"]

    res_get = client.get(f"/tasks/{task_id}")
    assert res_get.status_code == 200
    task = res_get.get_json()
    assert task["username"] == "user1"
    assert task["title"] == "Task 1"


def test_delete_task(client):
    # create
    client.post("/tasks", json={
        "username": "u",
        "title": "t",
        "description": "d",
        "deadline": "2026-02-01"
    })

    tasks = client.get("/tasks").get_json()
    task_id = tasks[0]["id"]

    res_del = client.delete(f"/tasks/{task_id}")
    assert res_del.status_code == 200

    res_get = client.get(f"/tasks/{task_id}")
    assert res_get.status_code == 404
