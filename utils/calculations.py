import pandas as pd


def completion_percentage(tasks: pd.DataFrame) -> float:
    if tasks.empty or "completed" not in tasks:
        return 0.0
    return round(float(tasks["completed"].fillna(False).astype(bool).mean() * 100), 1)


def tasks_by_discipline(tasks: pd.DataFrame) -> pd.DataFrame:
    if tasks.empty or "discipline" not in tasks:
        return pd.DataFrame(columns=["discipline", "total"])
    names = tasks["discipline"].fillna("").replace("", "Sem disciplina")
    return names.value_counts().rename_axis("discipline").reset_index(name="total")

