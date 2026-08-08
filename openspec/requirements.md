# Requisitos e rastreabilidade

| ID | Requisito | Implementacao | Validacao |
|---|---|---|---|
| AUTH-1 | Login por `/auth/login`, sessao e logout | `services/auth_service.py`, `utils/session.py` | testes unitarios e homologacao Xano |
| DISC-1 | CRUD de disciplinas | pagina Disciplinas + service | mock + homologacao Xano |
| TASK-1 | CRUD/status de tarefas | pagina Tarefas + service | mock + homologacao Xano |
| DASH-1 | metricas, progresso e barras | Dashboard + Pandas | testes de calculo |
| FILTER-1 | status e disciplina com multiselect | pagina Tarefas | testes de filtro |
| PDF-1 | relatorio semanal PDF | report service | assinatura `%PDF` |
| PERF-1 | cache seguro | cache por usuario/token hasheado, invalidado em mutacoes | revisao |
| SEC-1 | secrets fora do codigo | `st.secrets`, `.gitignore` | varredura |

Estados de UI obrigatorios: carregando, vazio, sucesso, erro, nao autorizado e falha de rede. Mensagens ao usuario nao incluem tokens, URLs internas ou stack traces.

