import json
import pytest
import requests
from integrations.xano_client import XanoClient, XanoError
from services.auth_service import authenticate, authenticate_local


class Response:
    def __init__(self, status=200, payload=None):
        self.status_code = status; self.ok = status < 400; self.content = b"" if payload is None else json.dumps(payload).encode(); self._payload = payload
    def json(self): return self._payload


class Session:
    def __init__(self, response=None, error=None): self.response=response; self.error=error; self.last=None
    def request(self, *args, **kwargs):
        self.last=(args, kwargs)
        if self.error: raise self.error
        return self.response


def test_authenticate_extracts_token_without_logging_it():
    session = Session(Response(payload={"authToken": "secret", "user": {"id": 1}}))
    token, user = authenticate(XanoClient("https://example.test", session=session), "/auth/login", "a@b.com", "pw")
    assert token == "secret" and user["id"] == 1
    assert session.last[1]["json"]["email"] == "a@b.com"


@pytest.mark.parametrize("status,kind", [(401,"unauthorized"),(403,"forbidden"),(404,"not_found"),(422,"validation"),(429,"rate_limit"),(500,"server")])
def test_safe_http_errors(status, kind):
    with pytest.raises(XanoError) as error:
        XanoClient("https://example.test", session=Session(Response(status))).get("/x", "token")
    assert error.value.kind == kind and "token" not in str(error.value)


def test_network_error():
    with pytest.raises(XanoError) as error:
        XanoClient("https://example.test", session=Session(error=requests.Timeout())).get("/x", "token")
    assert error.value.kind == "network"


def test_auth_rejects_non_string_token():
    with pytest.raises(XanoError) as error:
        authenticate(
            XanoClient("https://example.test", session=Session(Response(payload={"token": 123}))),
            "/auth/login", "a@b.com", "pw",
        )
    assert error.value.kind == "malformed_response"


def test_local_authentication_is_explicit_and_validates_credentials():
    config = {"enabled": True, "email": "teste@local", "password": "senha"}
    token, user = authenticate_local(config, "teste@local", "senha")
    assert token == "local-test-session" and user["local_mode"] is True
    with pytest.raises(ValueError):
        authenticate_local(config, "teste@local", "errada")
