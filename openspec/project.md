# EduTrack AI

## Visao do produto

Web app responsivo para estudantes autenticados organizarem disciplinas e tarefas e acompanharem o progresso academico com metricas, filtros, grafico e relatorio semanal em PDF.

## Fonte e escopo

A especificacao de negocio fornecida em 08/08/2026 e o requisito primario. A stack obrigatoria e Python, Streamlit, Pandas e Xano. Nao fazem parte do escopo: notificacoes push, app nativo, gamificacao, ranking, chat, pagamentos, calendario, marketplace ou IA generativa.

## Estado inicial

O projeto e construido do zero a partir da especificacao de negocio e deste OpenSpec. Nenhuma implementacao anterior ou historico Git integra a base tecnica adotada.

## Lacuna externa

Nao foram fornecidos URL, schema nem contratos reais do workspace Xano. A aplicacao usa caminhos configuraveis em secrets, com defaults explicitamente provisórios. A integracao real somente pode ser homologada apos preencher esses valores e confirmar payloads no Xano.
