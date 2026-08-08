from __future__ import annotations

from copy import deepcopy


class LocalClient:
    """Adaptador temporario em memoria para testar toda a UI sem Xano."""

    def __init__(self, state):
        self.state = state
        self.state.setdefault("local_disciplines", [])
        self.state.setdefault("local_tasks", [])

    @staticmethod
    def _resource(path: str) -> str:
        parts = [part for part in path.strip("/").split("/") if part]
        return parts[-2] if len(parts) > 1 and parts[-1].isdigit() else parts[-1]

    @staticmethod
    def _item_id(path: str) -> int | None:
        last = path.rstrip("/").rsplit("/", 1)[-1]
        return int(last) if last.isdigit() else None

    def get(self, path: str, token: str):
        resource = self._resource(path)
        return deepcopy(self.state.get(f"local_{resource}", []))

    def post(self, path: str, json: dict, token: str | None = None):
        resource = self._resource(path)
        key = f"local_{resource}"
        items = self.state.setdefault(key, [])
        next_id = max((int(item["id"]) for item in items), default=0) + 1
        item = {"id": next_id, **deepcopy(json)}
        items.append(item)
        return deepcopy(item)

    def patch(self, path: str, json: dict, token: str):
        resource, item_id = self._resource(path), self._item_id(path)
        for item in self.state.get(f"local_{resource}", []):
            if item.get("id") == item_id:
                item.update(deepcopy(json))
                return deepcopy(item)
        return None

    def delete(self, path: str, token: str):
        resource, item_id = self._resource(path), self._item_id(path)
        key = f"local_{resource}"
        self.state[key] = [item for item in self.state.get(key, []) if item.get("id") != item_id]
        if resource == "disciplines":
            self.state["local_tasks"] = [
                task for task in self.state.get("local_tasks", [])
                if task.get("discipline_id") != item_id
            ]
        return None
