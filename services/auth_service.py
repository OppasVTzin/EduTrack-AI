import hmac

from integrations.xano_client import XanoClient, XanoError


def authenticate(client: XanoClient, endpoint: str, email: str, password: str) -> tuple[str, dict]:
    if not email.strip() or not password:
        raise ValueError("Informe email e senha.")
    payload = client.post(endpoint, {"email": email.strip(), "password": password})
    if not isinstance(payload, dict):
        raise XanoError("malformed_response", "O login retornou uma resposta invalida.")
    token = payload.get("authToken") or payload.get("auth_token") or payload.get("token")
    if not isinstance(token, str) or not token.strip():
        raise XanoError("malformed_response", "O login nao retornou uma sessao valida.")
    user = payload.get("user") if isinstance(payload.get("user"), dict) else {}
    return token.strip(), user


def authenticate_local(config, email: str, password: str) -> tuple[str, dict]:
    if not config.get("enabled", False):
        raise ValueError("Login local desativado.")
    expected_email = str(config.get("email", ""))
    expected_password = str(config.get("password", ""))
    valid = hmac.compare_digest(email.strip(), expected_email) and hmac.compare_digest(
        password, expected_password
    )
    if not valid:
        raise ValueError("Email ou senha invalidos.")
    return "local-test-session", {"email": expected_email, "local_mode": True}
