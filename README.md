# EduTrack AI

Assistente educacional responsivo em Streamlit para gerenciar disciplinas, tarefas e progresso, persistidos no Xano.

## Funcionalidades

Login e sessão Xano, CRUD de disciplinas, criação/conclusão/exclusão de tarefas, dashboard com métricas e gráfico, filtros por status/disciplina e relatório semanal em PDF.

## Stack e arquitetura

Python, Streamlit, Pandas, Requests, ReportLab, pytest e Xano. A UI chama services, que usam um único `XanoClient`. Regras puras ficam em `utils/`; decisões e contratos estão em `openspec/`.

## Configuração

1. Crie e ative um ambiente virtual.
2. Execute `pip install -r requirements.txt`.
3. Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml`.
4. Informe a URL do grupo de APIs e confirme os paths reais do seu Xano.

O arquivo real de secrets é ignorado pelo Git. Não use tokens administrativos: o login armazena apenas o token do usuário na sessão Streamlit.

### Login local temporário

Enquanto o Xano está em construção, o arquivo local ignorado pelo Git habilita o usuário `teste@edutrack.local` com senha `teste123`. Esse modo não chama o Xano e mantém disciplinas e tarefas na sessão para testar toda a navegação, dashboard e PDF. Remova `[local_auth]` e o adaptador local ao integrar a autenticação real.

## Execução e testes

```bash
streamlit run app.py
pytest -q
```

Os testes são locais e mockam o Xano. A homologação final exige um workspace real, pois URL, schema e endpoints não foram fornecidos.

## Xano

O contrato configurável e as respostas aceitas estão em `openspec/api.md`. O Xano deve impor autenticação e ownership em todos os endpoints. Ajuste os nomes de campos na camada `models/normalizers.py` quando o schema real for confirmado.

## Deploy

No Streamlit Community Cloud, selecione `app.py`, instale pelo `requirements.txt` e cole o conteúdo de `secrets.toml` no painel de secrets. Não há dependência de armazenamento local persistente.
