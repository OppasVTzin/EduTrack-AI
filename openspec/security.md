# Seguranca

- URL e paths em `st.secrets`; token de usuario apenas em `st.session_state`.
- `.streamlit/secrets.toml` ignorado; exemplo sem credenciais reais versionado.
- timeout e TLS habilitados; nenhum fallback de autenticacao local.
- paginas protegidas antes de qualquer leitura.
- logout remove token, usuario e dados derivados.
- o Xano deve validar ownership em cada endpoint. A UI nao e fronteira de autorizacao.

