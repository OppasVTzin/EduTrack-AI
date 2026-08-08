import pandas as pd
from utils.calculations import completion_percentage, tasks_by_discipline
from utils.filters import filter_tasks


def sample():
    return pd.DataFrame([
        {"completed": True, "discipline": "Matematica"},
        {"completed": False, "discipline": "Historia"},
    ])


def test_completion_percentage_and_empty():
    assert completion_percentage(sample()) == 50.0
    assert completion_percentage(pd.DataFrame()) == 0.0


def test_group_and_filters():
    assert tasks_by_discipline(sample())["total"].sum() == 2
    assert len(filter_tasks(sample(), ["Pendente"], [])) == 1
    assert len(filter_tasks(sample(), [], ["Historia"])) == 1

