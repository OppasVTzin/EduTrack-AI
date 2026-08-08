from models.normalizers import extract_items, normalize_task


def list_tasks(client, endpoint, token):
    unique = {}
    for item in (normalize_task(x) for x in extract_items(client.get(endpoint, token))):
        if item["id"] is not None:
            unique[item["id"]] = item
    return list(unique.values())


def create_task(client, endpoint, token, title, discipline_id):
    if not title.strip(): raise ValueError("Informe o titulo da tarefa.")
    return client.post(endpoint, {"title": title.strip(), "discipline_id": discipline_id, "completed": False}, token)


def update_task(client, endpoint, token, item_id, data):
    return client.patch(f"{endpoint.rstrip('/')}/{item_id}", data, token)


def delete_task(client, endpoint, token, item_id):
    return client.delete(f"{endpoint.rstrip('/')}/{item_id}", token)
