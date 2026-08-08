import pandas as pd
import streamlit as st
from components.errors import show_error
from services import task_service
from utils.filters import filter_tasks


def render(client, endpoint, token, disciplines: pd.DataFrame, tasks: pd.DataFrame, refresh):
    st.title("Tarefas")
    st.caption("Acompanhe atividades pendentes e registre suas conclusões.")
    with st.sidebar.form("new_task", clear_on_submit=True):
        st.subheader("Nova tarefa")
        title = st.text_input("Titulo")
        discipline_rows = disciplines.to_dict("records") if not disciplines.empty else []
        discipline_index = st.selectbox(
            "Disciplina", range(len(discipline_rows)), disabled=not discipline_rows,
            format_func=lambda index: f"{discipline_rows[index]['name']} (ID {discipline_rows[index]['id']})",
        )
        if st.form_submit_button("Adicionar", disabled=not discipline_rows, use_container_width=True):
            try:
                discipline_id = discipline_rows[discipline_index]["id"]
                task_service.create_task(client, endpoint, token, title, discipline_id); refresh(); st.rerun()
            except Exception as exc: show_error(exc)
    statuses = st.multiselect("Status", ["Pendente", "Concluida"], default=["Pendente", "Concluida"])
    discipline_options = sorted(
        {str(value).strip() for value in tasks["discipline"].dropna() if str(value).strip()}
    ) if not tasks.empty else []
    discipline_filters = st.multiselect("Disciplina", discipline_options)
    shown = filter_tasks(tasks, statuses, discipline_filters) if not tasks.empty else tasks
    if shown.empty: st.info("Nenhuma tarefa corresponde aos filtros selecionados."); return
    for row in shown.to_dict("records"):
        cols = st.columns([5, 2, 1])
        cols[0].write(f"**{row['title']}**  \n{row.get('discipline') or 'Sem disciplina'}")
        checked = cols[1].checkbox("Concluída", value=row["completed"], key=f"done_{row['id']}")
        if checked != row["completed"]:
            try: task_service.update_task(client, endpoint, token, row["id"], {"completed": checked}); refresh(); st.rerun()
            except Exception as exc: show_error(exc)
        if cols[2].button("Excluir", key=f"delete_{row['id']}"):
            st.session_state["delete_task"] = row["id"]
    pending_delete = st.session_state.get("delete_task")
    if pending_delete is not None:
        st.warning("Confirme a exclusão da tarefa selecionada.")
        confirm, cancel = st.columns(2)
        if confirm.button("Confirmar exclusão da tarefa", type="primary"):
            try:
                task_service.delete_task(client, endpoint, token, pending_delete)
                st.session_state.pop("delete_task", None); refresh(); st.rerun()
            except Exception as exc: show_error(exc)
        if cancel.button("Cancelar"):
            st.session_state.pop("delete_task", None); st.rerun()
