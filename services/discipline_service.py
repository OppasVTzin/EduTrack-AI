from integrations.xano_client import XanoClient
from models.normalizers import extract_items, normalize_discipline


def list_disciplines(client: XanoClient, endpoint: str, token: str) -> list[dict]:
    unique = {}
    for item in (normalize_discipline(x) for x in extract_items(client.get(endpoint, token))):
        if item["id"] is not None:
            unique[item["id"]] = item
    return list(unique.values())


def create_discipline(client, endpoint, token, name):
    if not name.strip(): raise ValueError("Informe o nome da disciplina.")
    return client.post(endpoint, {"name": name.strip()}, token)


def update_discipline(client, endpoint, token, item_id, name):
    if not name.strip(): raise ValueError("Informe o nome da disciplina.")
    return client.patch(f"{endpoint.rstrip('/')}/{item_id}", {"name": name.strip()}, token)


def delete_discipline(client, endpoint, token, item_id):
    return client.delete(f"{endpoint.rstrip('/')}/{item_id}", token)
