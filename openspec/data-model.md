# Modelo de dados minimo

Modelo logico a confirmar no Xano:

- User: `id` (identificador), `name` (texto), `email` (texto). Senhas/tokens nao sao modelados no app.
- Discipline: `id` (identificador), `name` (texto obrigatorio), `user_id` (relacao com User, gerenciada/autorizada no Xano).
- Task: `id` (identificador), `title` (texto obrigatorio), `discipline_id` (relacao obrigatoria), `completed` (booleano), `due_date` (data opcional, somente se existir no Xano).

Aliases comuns em portugues/ingles sao normalizados na borda. Autorizacao e isolamento por usuario devem ser impostos pelo Xano, nunca por filtros do cliente.

