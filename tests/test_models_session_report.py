import pandas as pd
from models.normalizers import extract_items, normalize_task
from services.report_service import weekly_report
from utils.session import is_authenticated, login_session, logout_session


def test_normalization_variants():
    assert extract_items({"items": [{"id": 1}]}) == [{"id": 1}]
    assert normalize_task({"descricao": "Ler", "concluida": 1})["completed"] is True


def test_session_lifecycle():
    state = {
        "delete_task": 99,
        "widget_state": "old",
        "dark_mode": True,
        "local_disciplines": [],
    }
    login_session(state, "abc", {"id": 1})
    assert is_authenticated(state)
    logout_session(state)
    assert not is_authenticated(state)
    assert state == {"dark_mode": True, "local_disciplines": []}


def test_pdf_generation():
    disciplines = pd.DataFrame([{"id": 1, "name": "Matematica"}])
    tasks = pd.DataFrame([{"title": "Exercicios", "discipline": "Matematica", "completed": False}])
    result = weekly_report(disciplines, tasks)
    assert result.startswith(b"%PDF") and len(result) > 500
