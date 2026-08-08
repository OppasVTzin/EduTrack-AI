from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class XanoError(Exception):
    kind: str
    user_message: str
    status_code: int | None = None

    def __str__(self) -> str:
        return self.user_message


class XanoClient:
    def __init__(self, base_url: str, timeout: float = 10, session: requests.Session | None = None):
        if not base_url or "YOUR-" in base_url:
            raise ValueError("Configure a URL base do Xano nos secrets.")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

    def request(self, method: str, path: str, *, token: str | None = None, json: dict | None = None) -> Any:
        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            response = self.session.request(
                method, f"{self.base_url}/{path.lstrip('/')}", headers=headers,
                json=json, timeout=self.timeout,
            )
        except (requests.Timeout, requests.ConnectionError) as exc:
            raise XanoError("network", "Nao foi possivel conectar ao Xano. Tente novamente.") from exc
        except requests.RequestException as exc:
            raise XanoError("network", "Falha de comunicacao com o servico.") from exc

        if not response.ok:
            messages = {
                401: ("unauthorized", "Sua sessao expirou. Entre novamente."),
                403: ("forbidden", "Voce nao tem permissao para esta operacao."),
                404: ("not_found", "O recurso solicitado nao foi encontrado."),
                422: ("validation", "Revise os dados informados."),
                429: ("rate_limit", "Muitas solicitacoes. Aguarde e tente novamente."),
            }
            kind, message = messages.get(response.status_code, ("server", "O Xano esta indisponivel no momento."))
            raise XanoError(kind, message, response.status_code)
        if response.status_code == 204 or not response.content:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise XanoError("malformed_response", "O servico retornou uma resposta invalida.") from exc

    def get(self, path: str, token: str): return self.request("GET", path, token=token)
    def post(self, path: str, json: dict, token: str | None = None): return self.request("POST", path, token=token, json=json)
    def patch(self, path: str, json: dict, token: str): return self.request("PATCH", path, token=token, json=json)
    def delete(self, path: str, token: str): return self.request("DELETE", path, token=token)

