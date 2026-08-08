import streamlit as st
from integrations.xano_client import XanoError
from utils.session import logout_session


def show_error(error: Exception) -> None:
    if isinstance(error, XanoError):
        st.error(error.user_message)
        if error.kind == "unauthorized":
            logout_session(st.session_state)
            st.cache_data.clear()
            st.info("Entre novamente para continuar.")
            st.rerun()
    elif isinstance(error, ValueError):
        st.warning(str(error))
    else:
        st.error("Nao foi possivel concluir a operacao. Tente novamente.")
