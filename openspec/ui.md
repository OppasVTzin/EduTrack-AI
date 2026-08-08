# UI

Login e a unica tela publica. Depois do login, navegacao lateral: Dashboard, Disciplinas, Tarefas e Relatorios, seguida de logout. Dashboard abre por default. Formularios de criacao ficam na sidebar da pagina correspondente. Filtros de tarefas usam dois `multiselect`.

Layout wide, colunas que empilham naturalmente em telas estreitas e componentes nativos do Streamlit. Confirmacao e exigida antes de exclusao.

## Temas e login

O usuario pode alternar entre modo claro e escuro no login e na sidebar; a escolha permanece durante a sessao. O tema usa tokens de cor com contraste consistente, superficies, metricas e formularios harmonizados. A tela de login apresenta somente a marca e a proposta do EduTrack AI, sem expor detalhes do mecanismo temporario de autenticacao. O login local e desativado removendo ou definindo `local_auth.enabled = false` quando a autenticacao oficial estiver pronta.
