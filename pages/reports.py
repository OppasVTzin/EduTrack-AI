import streamlit as st
from services.report_service import weekly_report


def render(disciplines, tasks):
    st.title("Relatório semanal")
    st.caption("Leve com você um resumo objetivo da sua semana acadêmica.")
    st.write("O documento reúne disciplinas, tarefas, pendências e progresso atuais.")
    pdf = weekly_report(disciplines, tasks)
    st.download_button("Baixar relatório semanal", pdf, "edutrack_relatorio_semanal.pdf", "application/pdf", use_container_width=True)
