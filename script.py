import pandas as pd
import streamlit as st

st.set_page_config(page_title="EduTrack AI", page_icon="📚", layout="wide")


def aplicar_estilos():
    st.markdown(
        """
        <style>
        :root {
            --bg: #f4f7ff;
            --card: rgba(255,255,255,0.95);
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --accent: #38bdf8;
            --text: #0f172a;
            --muted: #64748b;
        }

        .stApp {
            background: linear-gradient(135deg, #eef4ff 0%, #f8fbff 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .login-card {
            max-width: 720px;
            margin: 0 auto 1rem auto;
            padding: 2rem;
            border-radius: 24px;
            background: var(--card);
            box-shadow: 0 18px 44px rgba(15, 23, 42, 0.08);
            border: 1px solid rgba(148, 163, 184, 0.2);
        }

        .badge {
            display: inline-block;
            margin-bottom: 0.8rem;
            padding: 6px 12px;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.04rem;
        }

        h1 {
            color: #1e3a8a;
            margin-bottom: 0.4rem;
            font-weight: 800;
            text-align: center;
        }

        .subtitle {
            color: var(--muted);
            text-align: center;
            margin-bottom: 1.3rem;
        }

        .stTextInput > div > div > input,
        .stSelectbox > div > div > div {
            border-radius: 12px;
            border: 1px solid #cbd5e1;
            padding: 10px 12px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
        }

        .stButton > button {
            width: 100%;
            border: none;
            border-radius: 999px;
            height: 44px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            font-weight: 700;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.2);
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, var(--primary-dark) 0%, #0ea5e9 100%);
            transform: translateY(-1px);
        }

        .highlight-card {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.12) 0%, rgba(56, 189, 248, 0.18) 100%);
            border: 1px solid rgba(37, 99, 235, 0.15);
            border-radius: 22px;
            padding: 1.2rem 1.3rem;
            margin-bottom: 1rem;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.08);
        }

        .info-pill {
            display: inline-block;
            padding: 0.35rem 0.8rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.9);
            color: var(--primary);
            font-size: 0.85rem;
            font-weight: 700;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .hero-panel {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 45%, #2563eb 100%);
            border-radius: 28px;
            padding: 2rem;
            color: white;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.20);
            margin-bottom: 1.25rem;
        }

        .hero-panel h1 {
            color: white;
            font-size: 2rem;
            text-align: left;
        }

        .hero-panel .subtitle {
            color: rgba(255,255,255,0.85);
            text-align: left;
            margin-bottom: 1rem;
        }

        .glass-form {
            background: rgba(255,255,255,0.92);
            border-radius: 22px;
            padding: 1.2rem;
            box-shadow: 0 14px 36px rgba(15, 23, 42, 0.08);
            border: 1px solid rgba(148, 163, 184, 0.18);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }

        [data-testid="stSidebar"] * {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def carregar_dados():
    disciplinas = pd.DataFrame(
        [
            {"id": 1, "nome": "Matemática", "professor": "Ana Paula", "cor": "#2563eb"},
            {"id": 2, "nome": "História", "professor": "Carlos Mendes", "cor": "#16a34a"},
            {"id": 3, "nome": "Biologia", "professor": "Larissa Souza", "cor": "#f59e0b"},
        ]
    )
    tarefas = pd.DataFrame(
        [
            {"id": 1, "descricao": "Revisar funções", "disciplina": "Matemática", "prioridade": "Alta", "concluida": False},
            {"id": 2, "descricao": "Resumo da Revolução Francesa", "disciplina": "História", "prioridade": "Média", "concluida": False},
            {"id": 3, "descricao": "Estudar células", "disciplina": "Biologia", "prioridade": "Baixa", "concluida": True},
            {"id": 4, "descricao": "Exercícios de álgebra", "disciplina": "Matemática", "prioridade": "Alta", "concluida": True},
        ]
    )
    return disciplinas, tarefas


def inicializar_estado():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if "tela_atual" not in st.session_state:
        st.session_state.tela_atual = "login"
    if "usuario" not in st.session_state:
        st.session_state.usuario = "estudante"
    if "disciplinas" not in st.session_state:
        disciplinas, tarefas = carregar_dados()
        st.session_state.disciplinas = disciplinas
        st.session_state.tarefas = tarefas


def render_header(title, subtitle):
    st.markdown(
        f"""
        <div class="login-card">
            <div class="badge">EduTrack AI</div>
            <h1>{title}</h1>
            <p class="subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.title("EduTrack AI")
        st.caption("Assistente educacional personalizado")

        if st.button("Dashboard", use_container_width=True):
            st.session_state.tela_atual = "dashboard"
            st.rerun()
        if st.button("Disciplinas", use_container_width=True):
            st.session_state.tela_atual = "disciplinas"
            st.rerun()
        if st.button("Tarefas", use_container_width=True):
            st.session_state.tela_atual = "tarefas"
            st.rerun()
        if st.button("Relatórios", use_container_width=True):
            st.session_state.tela_atual = "relatorios"
            st.rerun()

        st.divider()
        if st.button("Sair", use_container_width=True):
            st.session_state.autenticado = False
            st.session_state.tela_atual = "login"
            st.rerun()


def tela_login():
    st.markdown(
        """
        <div class="hero-panel">
            <div class="badge">EduTrack AI</div>
            <h1>Transforme seu estudo em uma experiência inteligente</h1>
            <p class="subtitle">Organize matérias, acompanhe tarefas e veja seu progresso com um painel moderno e envolvente.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([1.25, 1], gap="large")

    with col_left:
        st.markdown(
            """
            <div class="highlight-card">
                <strong>✨ Acesso premium para o seu planejamento</strong><br>
                Tudo o que você precisa para manter foco, disciplina e clareza em um só lugar.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div class='info-pill'>📚 Disciplinas</div><div class='info-pill'>✅ Tarefas</div><div class='info-pill'>📈 Progresso</div>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Organização", "100%")
        col2.metric("Foco", "+25%")
        col3.metric("Clareza", "Total")

    with col_right:
        st.markdown("<div class='glass-form'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; color:#1e3a8a;'>Entrar no sistema</h3>", unsafe_allow_html=True)
        st.info("Demo: usuário admin / senha admin")

        with st.form("form_login"):
            username = st.text_input("Usuário", placeholder="Digite seu usuário")
            password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            submitted = st.form_submit_button("Entrar", use_container_width=True)

        if submitted:
            if username == "admin" and password == "admin":
                st.session_state.autenticado = True
                st.session_state.tela_atual = "dashboard"
                st.session_state.usuario = username
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

        st.markdown("</div>", unsafe_allow_html=True)


def tela_dashboard():
    render_header("📈 Dashboard", "Veja seu progresso e pendências de forma clara.")

    disciplinas = st.session_state.disciplinas.copy()
    tarefas = st.session_state.tarefas.copy()
    tarefas["status"] = tarefas["concluida"].map({True: "Concluída", False: "Pendente"})

    total_disciplinas = len(disciplinas)
    pendentes = int((~tarefas["concluida"]).sum())
    progresso = round(tarefas["concluida"].mean() * 100, 1) if not tarefas.empty else 0
    urgentes = tarefas[(tarefas["concluida"] == False) & (tarefas["prioridade"] == "Alta")]
    disciplina_em_foco = pendentes and urgentes["disciplina"].value_counts().idxmax() or "Nenhuma"

    st.markdown(
        f"""
        <div class="highlight-card">
            <strong>Olá, {st.session_state.usuario}!</strong><br>
            Você tem <strong>{pendentes}</strong> tarefas pendentes e <strong>{progresso}%</strong> de progresso geral.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de disciplinas", total_disciplinas)
    col2.metric("Tarefas pendentes", pendentes)
    col3.metric("Prioridades altas", len(urgentes))

    st.progress(progresso / 100)

    tab1, tab2, tab3 = st.tabs(["Resumo", "Progresso", "Planejamento"])

    with tab1:
        st.subheader("Resumo do dia")
        st.write("O melhor próximo passo é concluir a tarefa mais urgente e manter o ritmo constante.")

    with tab2:
        st.subheader("Tarefas por disciplina")
        grafico = tarefas.groupby("disciplina").size().reset_index(name="total")
        st.bar_chart(grafico.set_index("disciplina"))

    with tab3:
        st.subheader("Próximo foco")
        if not urgentes.empty:
            st.write(f"Disciplina com mais foco agora: {disciplina_em_foco}")
            st.dataframe(urgentes[["descricao", "disciplina", "prioridade"]], use_container_width=True)
        else:
            st.success("Parabéns! Você está em dia com suas tarefas.")

    st.subheader("Tarefas recentes")
    filtros = st.multiselect(
        "Filtrar por status",
        options=["Pendente", "Concluída"],
        default=["Pendente", "Concluída"],
    )
    filtradas = tarefas[tarefas["status"].isin(filtros)]
    st.dataframe(filtradas[["descricao", "disciplina", "prioridade", "status"]], use_container_width=True)


def tela_disciplinas():
    render_header("🗂️ Disciplinas", "Gerencie matérias, professores e cores.")

    disciplinas = st.session_state.disciplinas.copy()

    with st.form("form_disciplina"):
        nome = st.text_input("Nome da disciplina")
        professor = st.text_input("Professor")
        cor = st.text_input("Cor (hex)", value="#2563eb")
        submitted = st.form_submit_button("Adicionar disciplina", use_container_width=True)

        if submitted and nome.strip():
            novo_id = int(disciplinas["id"].max()) + 1 if not disciplinas.empty else 1
            disciplinas.loc[len(disciplinas)] = [novo_id, nome.strip(), professor.strip(), cor.strip()]
            st.session_state.disciplinas = disciplinas
            st.success("Disciplina adicionada com sucesso!")
            st.rerun()

    st.subheader("Lista de disciplinas")
    editadas = st.data_editor(
        disciplinas,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "id": "ID",
            "nome": "Disciplina",
            "professor": "Professor",
            "cor": "Cor",
        },
    )

    if not editadas.equals(disciplinas):
        st.session_state.disciplinas = editadas
        st.caption("Alterações salvas localmente.")


def tela_tarefas():
    render_header("✅ Tarefas", "Organize atividades por disciplina e status.")

    disciplinas = st.session_state.disciplinas.copy()
    tarefas = st.session_state.tarefas.copy()

    with st.form("form_tarefa"):
        descricao = st.text_input("Descrição da tarefa")
        disciplina = st.selectbox("Disciplina", disciplinas["nome"].tolist())
        prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
        submitted = st.form_submit_button("Adicionar tarefa", use_container_width=True)

        if submitted and descricao.strip():
            novo_id = int(tarefas["id"].max()) + 1 if not tarefas.empty else 1
            tarefas.loc[len(tarefas)] = [novo_id, descricao.strip(), disciplina, prioridade, False]
            st.session_state.tarefas = tarefas
            st.success("Tarefa adicionada com sucesso!")
            st.rerun()

    st.checkbox("Mostrar apenas pendentes", value=True, key="mostrar_pendentes")
    tarefas_exibicao = tarefas[tarefas["concluida"] == False] if st.session_state.mostrar_pendentes else tarefas

    st.subheader("Gerenciar tarefas")
    editadas = st.data_editor(
        tarefas_exibicao,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "id": "ID",
            "descricao": "Descrição",
            "disciplina": "Disciplina",
            "prioridade": "Prioridade",
            "concluida": "Concluída",
        },
    )

    if not editadas.equals(tarefas_exibicao):
        st.session_state.tarefas = pd.concat([tarefas[~tarefas["id"].isin(editadas["id"])], editadas], ignore_index=True)
        st.caption("Status das tarefas atualizado.")


def tela_relatorios():
    render_header("📄 Relatórios", "Baixe um resumo semanal do seu desempenho.")

    disciplinas = len(st.session_state.disciplinas)
    pendentes = int((~st.session_state.tarefas["concluida"]).sum())
    resumo = f"Resumo semanal EduTrack AI\nDisciplinas: {disciplinas}\nTarefas pendentes: {pendentes}\n"

    st.write(resumo)
    st.download_button(
        label="Baixar relatório (.txt)",
        data=resumo,
        file_name="relatorio_semanal.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.caption("No futuro, esta etapa pode evoluir para um PDF com ReportLab.")


def main():
    aplicar_estilos()
    inicializar_estado()

    if not st.session_state.autenticado:
        tela_login()
    else:
        render_sidebar()
        if st.session_state.tela_atual == "disciplinas":
            tela_disciplinas()
        elif st.session_state.tela_atual == "tarefas":
            tela_tarefas()
        elif st.session_state.tela_atual == "relatorios":
            tela_relatorios()
        else:
            tela_dashboard()


if __name__ == "__main__":
    main()