import pandas as pd


def filter_tasks(tasks: pd.DataFrame, statuses: list[str], disciplines: list[str]) -> pd.DataFrame:
    result = tasks.copy()
    if statuses:
        wanted = {value == "Concluida" for value in statuses}
        result = result[result["completed"].astype(bool).isin(wanted)]
    if disciplines:
        result = result[result["discipline"].isin(disciplines)]
    return result

