# Testes e validacao

Testes unitarios sem backend real cobrem a borda HTTP por mocks, autenticacao, sessao pura, progresso, filtros, normalizacao, PDF e inicializacao Streamlit. O backend Xano esta explicitamente fora da etapa atual porque segue em construcao pela equipe de dados; endpoints, schemas, persistencia e homologacao remota nao fazem parte do aceite de Bug Fixes.

Deploy: Streamlit Community Cloud, `app.py` como entrypoint, secrets configurados no painel e dependencias pinadas por faixa compativel.
