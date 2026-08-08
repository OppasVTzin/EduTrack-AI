# Arquitetura

`app.py` compoe navegacao e paginas. `pages/` renderiza Streamlit; `services/` aplica regras; `integrations/xano_client.py` concentra HTTP; `utils/` contem sessao, filtros e calculos; `models/` normaliza payloads. Dependencias apontam UI -> services -> XanoClient.

Leituras autenticadas usam `st.cache_data` com o token bruto excluido da chave e uma identidade SHA-256 como chave opaca, alem de TTL curto. Tokens nunca sao retornados nem exibidos. Toda mutacao limpa o cache.

## Decisoes

- ADR-001: iniciar uma arquitetura modular do zero, orientada pela especificacao.
- ADR-002: parametrizar endpoints e nomes de campos, pois o contrato real do Xano esta ausente.
- ADR-003: usar `reportlab` para PDF em memoria, compativel com Streamlit Community Cloud.
