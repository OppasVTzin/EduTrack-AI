# Contrato de API configuravel

Os caminhos abaixo sao defaults provisórios, nao contratos Xano confirmados:

| Operacao | Metodo/caminho default |
|---|---|
| Login | `POST /auth/login` |
| Disciplinas | `GET/POST /disciplines` |
| Disciplina | `PATCH/DELETE /disciplines/{id}` |
| Tarefas | `GET/POST /tasks` |
| Tarefa | `PATCH/DELETE /tasks/{id}` |

Login envia `email` e `password`; o token e lido de `authToken`, `auth_token` ou `token`. Listas podem ser arrays ou estar em `items`, `data` ou `result`. Os paths sao configurados em `[xano.endpoints]`.

Erros HTTP sao convertidos em categorias seguras: unauthorized (401), forbidden (403), not_found (404), validation (422), rate_limit (429), server (5xx), network e malformed_response.

