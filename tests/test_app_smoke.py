from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_app_starts_without_local_secrets():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py", default_timeout=10).run()
    assert not app.exception
    assert app.subheader[0].value == "Boas-vindas"
    app.toggle[0].set_value(True).run()
    assert app.session_state["dark_mode"] is True
    assert not app.exception


def test_local_login_and_logout_flow():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py", default_timeout=10).run()
    app.text_input[0].input("teste@edutrack.local")
    app.text_input[1].input("teste123")
    app.button[0].click().run()
    assert not app.exception
    assert any(title.value.startswith("Olá, teste") for title in app.title)
    assert app.session_state["user"]["local_mode"] is True
    app.button[0].click().run()
    assert not app.exception
    assert any(item.value == "Boas-vindas" for item in app.subheader)
