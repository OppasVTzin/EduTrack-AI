from integrations.local_client import LocalClient


def test_local_crud_persists_in_shared_session_state():
    state = {}
    client = LocalClient(state)
    discipline = client.post("/disciplines", {"name": "Matemática"}, "local")
    task = client.post(
        "/tasks",
        {"title": "Exercícios", "discipline_id": discipline["id"], "completed": False},
        "local",
    )
    client.patch(f"/tasks/{task['id']}", {"completed": True}, "local")

    recreated_client = LocalClient(state)
    assert recreated_client.get("/disciplines", "local")[0]["name"] == "Matemática"
    assert recreated_client.get("/tasks", "local")[0]["completed"] is True


def test_deleting_discipline_cascades_local_test_tasks():
    state = {
        "local_disciplines": [{"id": 1, "name": "História"}],
        "local_tasks": [{"id": 1, "title": "Resumo", "discipline_id": 1}],
    }
    LocalClient(state).delete("/disciplines/1", "local")
    assert state["local_disciplines"] == []
    assert state["local_tasks"] == []
