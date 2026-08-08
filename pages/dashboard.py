import pandas as pd
import streamlit as st
from utils.calculations import completion_percentage, tasks_by_discipline


def render(disciplines: pd.DataFrame, tasks: pd.DataFrame, user: dict | None = None):
    identity = (user or {}).get("name") or (user or {}).get("email", "Estudante").split("@")[0]
    st.markdown('<div class="edutrack-eyebrow">Visão geral</div>', unsafe_allow_html=True)
    st.title(f"Olá, {identity} 👋")
    st.caption("Aqui está o panorama da sua jornada acadêmica hoje.")
    pending = 0 if tasks.empty else int((~tasks["completed"].astype(bool)).sum())
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de disciplinas", len(disciplines))
    c2.metric("Tarefas pendentes", pending)
    c3.metric("Progresso", f"{completion_percentage(tasks):.1f}%")
    progress = completion_percentage(tasks)
    st.progress(progress / 100, text=f"{progress:.1f}% das tarefas concluídas")
    if tasks.empty:
        st.info("Comece criando uma disciplina e sua primeira tarefa.")
    elif pending:
        st.warning(f"Você tem {pending} {'tarefa pendente' if pending == 1 else 'tarefas pendentes'}. Um passo de cada vez.")
    else:
        st.success("Tudo concluído. Excelente ritmo!")
    st.subheader("Tarefas por disciplina")
    chart = tasks_by_discipline(tasks)
    if chart.empty: st.info("Seu gráfico aparecerá aqui quando houver tarefas cadastradas.")
    else: st.bar_chart(chart.set_index("discipline"))
