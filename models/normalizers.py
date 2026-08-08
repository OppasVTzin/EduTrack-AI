from typing import Any
import math

import pandas as pd


def extract_items(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("items", "data", "result"):
            nested = payload.get(key)
            if isinstance(nested, list):
                return [item for item in nested if isinstance(item, dict)]
            if isinstance(nested, dict):
                items = extract_items(nested)
                if items:
                    return items
    return []


def normalize_discipline(item: dict) -> dict:
    return {"id": item.get("id"), "name": as_text(item.get("name", item.get("nome", "")))}


def as_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def as_boolean(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return False
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "sim", "concluida", "concluída"}
    return False


def normalize_task(item: dict) -> dict:
    completed = item.get("completed", item.get("concluida", False))
    discipline = item.get("discipline_name", item.get("disciplina", ""))
    if isinstance(item.get("discipline"), dict):
        discipline = item["discipline"].get("name", item["discipline"].get("nome", discipline))
    return {
        "id": item.get("id"),
        "title": as_text(item.get("title", item.get("descricao", item.get("name", "")))),
        "discipline_id": item.get("discipline_id", item.get("disciplina_id")),
        "discipline": as_text(discipline),
        "completed": as_boolean(completed),
        "due_date": item.get("due_date", item.get("data_entrega")),
    }


def attach_discipline_names(tasks: pd.DataFrame, disciplines: pd.DataFrame) -> pd.DataFrame:
    result = tasks.copy()
    if result.empty or disciplines.empty or "discipline_id" not in result or "id" not in disciplines:
        return result
    names = disciplines.dropna(subset=["id"]).drop_duplicates("id").set_index("id")["name"]
    missing = result["discipline"].isna() | result["discipline"].astype(str).str.strip().eq("")
    result.loc[missing, "discipline"] = result.loc[missing, "discipline_id"].map(names)
    return result
