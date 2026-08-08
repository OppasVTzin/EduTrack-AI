import pandas as pd

from models.normalizers import attach_discipline_names, extract_items, normalize_task
from services.report_service import weekly_report
from utils.session import is_authenticated


def test_string_false_is_not_truthy():
    assert normalize_task({"completed": "false"})["completed"] is False
    assert normalize_task({"completed": "0"})["completed"] is False
    assert normalize_task({"completed": "true"})["completed"] is True


def test_report_accepts_unicode_user_content():
    disciplines = pd.DataFrame([{"id": 1, "name": "Programacao"}])
    tasks = pd.DataFrame(
        [{"title": "Revisao 🚀 漢字", "discipline": "Programacao", "completed": False}]
    )
    assert weekly_report(disciplines, tasks).startswith(b"%PDF")


def test_nested_paginated_payload_is_extracted():
    assert extract_items({"data": {"items": [{"id": 7}]}}) == [{"id": 7}]


def test_missing_discipline_name_is_joined_by_id_with_duplicate_names_allowed():
    tasks = pd.DataFrame(
        [{"id": 1, "discipline_id": 20, "discipline": "", "completed": False}]
    )
    disciplines = pd.DataFrame(
        [{"id": 10, "name": "Calculo"}, {"id": 20, "name": "Calculo"}]
    )
    result = attach_discipline_names(tasks, disciplines)
    assert result.iloc[0]["discipline"] == "Calculo"


def test_non_string_session_token_is_not_authenticated():
    assert not is_authenticated({"auth_token": 123})
