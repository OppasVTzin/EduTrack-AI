import pandas as pd
import streamlit as st
from components.errors import show_error
from services import discipline_service


def render(client, endpoint, token, disciplines: pd.DataFrame, refresh):
    st.title("Disciplinas")
    st.caption("Organize as matérias que fazem parte da sua rotina de estudos.")
    with st.sidebar.form("new_discipline", clear_on_submit=True):
        st.subheader("Nova disciplina")
        name = st.text_input("Nome")
        if st.form_submit_button("Adicionar", use_container_width=True):
            try: discipline_service.create_discipline(client, endpoint, token, name); refresh(); st.rerun()
            except Exception as exc: show_error(exc)
    if disciplines.empty:
        st.info("Nenhuma disciplina cadastrada. Use o formulário lateral para começar."); return
    st.dataframe(disciplines, hide_index=True, use_container_width=True)
    rows = disciplines.to_dict("records")
    selected_index = st.selectbox(
        "Selecionar disciplina",
        range(len(rows)),
        format_func=lambda index: f"{rows[index]['name']} (ID {rows[index]['id']})",
    )
    selected = rows[selected_index]
    new_name = st.text_input(
        "Novo nome", value=selected["name"], key=f"edit_discipline_name_{selected['id']}"
    )
    c1, c2 = st.columns(2)
    if c1.button("Salvar alteração", type="primary", use_container_width=True):
        try: discipline_service.update_discipline(client, endpoint, token, selected["id"], new_name); refresh(); st.rerun()
        except Exception as exc: show_error(exc)
    confirm = st.checkbox(
        "Confirmo a exclusão desta disciplina",
        key=f"confirm_delete_discipline_{selected['id']}",
    )
    if c2.button("Excluir", disabled=not confirm, use_container_width=True):
        try: discipline_service.delete_discipline(client, endpoint, token, selected["id"]); refresh(); st.rerun()
        except Exception as exc: show_error(exc)
