def is_authenticated(state) -> bool:
    token = state.get("auth_token")
    return isinstance(token, str) and bool(token.strip())


def login_session(state, token: str, user: dict | None = None) -> None:
    if not isinstance(token, str) or not token.strip():
        raise ValueError("Token de sessao invalido.")
    state["auth_token"] = token.strip()
    state["user"] = user or {}


def logout_session(state) -> None:
    preserved = {
        key: value for key, value in state.items()
        if key == "dark_mode" or key.startswith("local_")
    }
    state.clear()
    state.update(preserved)
