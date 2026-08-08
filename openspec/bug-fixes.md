# Etapa de Bug Fixes

## Escopo

Auditoria do cliente Python/Streamlit, sem validar ou alterar o backend Xano em construcao.

## Bugs confirmados e corrigidos

| ID | Falha | Correcao | Regressao |
|---|---|---|---|
| BF-001 | App quebrava sem `secrets.toml` | estado de login inicia e informa configuracao somente ao autenticar | `test_app_smoke.py` |
| BF-002 | string `false` era convertida para `True` | conversor booleano explicito | `test_bug_regressions.py` |
| BF-003 | payload paginado/aninhado virava lista vazia | extracao recursiva controlada | `test_bug_regressions.py` |
| BF-004 | tarefa apenas com `discipline_id` ficava sem nome | join local por ID | `test_bug_regressions.py` |
| BF-005 | nomes duplicados selecionavam registro errado | seletores usam indice/ID e exibem ID | cobertura por regras e smoke |
| BF-006 | confirmacao podia migrar para outra disciplina | chave de widget por ID | revisao de UI |
| BF-007 | campo de nome ficava preso a selecao anterior | chave de widget por ID | revisao de UI |
| BF-008 | IDs duplicados quebravam chaves de widgets | deduplicacao na borda por ID | testes de service |
| BF-009 | falha de tarefas bloqueava Disciplinas | caches/leitura isolados por recurso | smoke e revisao |
| BF-010 | exclusao perdia alvo apos falha e nao tinha cancelamento | alvo removido apenas no sucesso; botao cancelar | revisao de UI |
| BF-011 | 401 mantinha tela protegida ate nova interacao | limpa sessao/cache e rerun imediato | teste de sessao + revisao |
| BF-012 | logout preservava exclusao/widget do usuario anterior | limpeza integral do estado de sessao | `test_models_session_report.py` |
| BF-013 | token nao textual podia ser tratado como autenticado | validacao estrita de token na sessao | `test_bug_regressions.py` |

## Fora de escopo

Contratos, schemas, autorizacao, disponibilidade, performance e consistencia do Xano. Esses itens serao homologados quando a equipe de dados disponibilizar o backend.

## Login local temporario

Enquanto o Xano esta em construcao, `[local_auth]` em `secrets.toml` habilita credenciais locais de teste. A sessao recebe `local_mode=true`, nao realiza chamadas remotas e usa `LocalClient` para tornar Disciplinas, Tarefas, Dashboard e PDF navegaveis. Dados locais e preferencia de tema sobrevivem a reruns e ao logout de teste; autenticacao e estados transitorios sao removidos. Para remover o mecanismo, apague a secao `local_auth`, `authenticate_local`, `LocalClient` e o ramo `local_mode` de `app.py`.
