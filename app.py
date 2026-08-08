from __future__ import annotations

import hashlib

import pandas as pd
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

from components.errors import show_error
from components.theme import apply_theme, theme_toggle
from integrations.xano_client import XanoClient
from integrations.local_client import LocalClient
from pages import dashboard, disciplines, reports, tasks
from services.auth_service import authenticate, authenticate_local
from services.discipline_service import list_disciplines
from services.task_service import list_tasks
from models.normalizers import attach_discipline_names
from utils.session import is_authenticated, login_session, logout_session

st.set_page_config(page_title="EduTrack AI", page_icon="📚", layout="wide")


def settings():
    try:
        config = st.secrets.get("xano", {})
        local_auth = st.secrets.get("local_auth", {})
    except StreamlitSecretNotFoundError:
        config = {}
        local_auth = {}
    endpoints = config.get("endpoints", {})
    return config, local_auth, {
        "login": endpoints.get("login", "/auth/login"),
        "disciplines": endpoints.get("disciplines", "/disciplines"),
        "tasks": endpoints.get("tasks", "/tasks"),
    }


def make_client(config):
    return XanoClient(str(config.get("base_url", "")), float(config.get("timeout", 10)))


def token_key(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


@st.cache_data(ttl=60, show_spinner=False)
def cached_disciplines(base_url, timeout, endpoint, _token, cache_identity):
    client = XanoClient(base_url, timeout)
    return list_disciplines(client, endpoint, _token)


@st.cache_data(ttl=60, show_spinner=False)
def cached_tasks(base_url, timeout, endpoint, _token, cache_identity):
    client = XanoClient(base_url, timeout)
    return list_tasks(client, endpoint, _token)


def login_view(config, local_auth, endpoints):
    top_left, top_right = st.columns([5, 1])
    with top_left:
        st.markdown('<div class="edutrack-brand">📚 EduTrack AI</div>', unsafe_allow_html=True)
    with top_right:
        theme_toggle()
    st.markdown(
        """
        <section class="edutrack-hero">
            <div style="font-weight:800;opacity:.85;margin-bottom:.6rem">ASSISTENTE EDUCACIONAL</div>
            <h1>Organize seus estudos.<br>Enxergue seu progresso.</h1>
            <p>Disciplinas, tarefas e evolução acadêmica reunidas em uma experiência simples e objetiva.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    _, login_column, _ = st.columns([1, 1.25, 1])
    with login_column, st.container(border=True):
        st.subheader("Boas-vindas")
        st.caption("Entre para acessar seu painel de estudos.")
        with st.form("login"):
            email = st.text_input("Email", placeholder="voce@email.com")
            password = st.text_input("Senha", type="password", placeholder="Sua senha")
            submitted = st.form_submit_button("Entrar", use_container_width=True)
    if submitted:
        try:
            if local_auth.get("enabled", False):
                token, user = authenticate_local(local_auth, email, password)
            else:
                token, user = authenticate(make_client(config), endpoints["login"], email, password)
            login_session(st.session_state, token, user)
            st.rerun()
        except Exception as exc:
            show_error(exc)


def main():
    apply_theme()
    config, local_auth, endpoints = settings()
    if not is_authenticated(st.session_state):
        login_view(config, local_auth, endpoints); return
    token = st.session_state["auth_token"]
    local_mode = bool(st.session_state.get("user", {}).get("local_mode"))
    with st.sidebar:
        st.markdown('<div class="edutrack-brand">📚 EduTrack AI</div>', unsafe_allow_html=True)
        user = st.session_state.get("user", {})
        st.caption(user.get("name") or user.get("email") or "Estudante")
        st.divider()
        navigation = {
            "◉  Dashboard": "Dashboard",
            "▦  Disciplinas": "Disciplinas",
            "✓  Tarefas": "Tarefas",
            "↧  Relatórios": "Relatórios",
        }
        section_label = st.radio("Navegação", list(navigation), label_visibility="collapsed")
        section = navigation[section_label]
        st.divider()
        theme_toggle(sidebar=True)
        if st.button("Sair", use_container_width=True):
            logout_session(st.session_state); st.cache_data.clear(); st.rerun()
    try:
        if local_mode:
            client = LocalClient(st.session_state)
            local_endpoints = {"disciplines": "/disciplines", "tasks": "/tasks"}
            raw_disciplines = list_disciplines(client, local_endpoints["disciplines"], token)
            raw_tasks = list_tasks(client, local_endpoints["tasks"], token)
            discipline_df = pd.DataFrame(raw_disciplines, columns=["id", "name"])
            task_df = pd.DataFrame(raw_tasks, columns=["id", "title", "discipline_id", "discipline", "completed", "due_date"])
            task_df = attach_discipline_names(task_df, discipline_df)
            refresh = lambda: None
            if section == "Disciplinas":
                disciplines.render(client, local_endpoints["disciplines"], token, discipline_df, refresh)
            elif section == "Tarefas":
                tasks.render(client, local_endpoints["tasks"], token, discipline_df, task_df, refresh)
            elif section == "Relatórios":
                reports.render(discipline_df, task_df)
            else:
                dashboard.render(discipline_df, task_df, st.session_state.get("user", {}))
            return
        base_url = str(config.get("base_url", "")); timeout = float(config.get("timeout", 10))
        identity = token_key(token)
        raw_disciplines = cached_disciplines(base_url, timeout, endpoints["disciplines"], token, identity)
        discipline_df = pd.DataFrame(raw_disciplines, columns=["id", "name"])
        client = make_client(config)
        refresh = st.cache_data.clear
        if section == "Disciplinas":
            disciplines.render(client, endpoints["disciplines"], token, discipline_df, refresh)
            return
        raw_tasks = cached_tasks(base_url, timeout, endpoints["tasks"], token, identity)
        task_df = pd.DataFrame(raw_tasks, columns=["id", "title", "discipline_id", "discipline", "completed", "due_date"])
        task_df = attach_discipline_names(task_df, discipline_df)
        if section == "Tarefas": tasks.render(client, endpoints["tasks"], token, discipline_df, task_df, refresh)
        elif section == "Relatórios": reports.render(discipline_df, task_df)
        else: dashboard.render(discipline_df, task_df, st.session_state.get("user", {}))
    except Exception as exc:
        show_error(exc)
        if st.button("Tentar novamente"): st.cache_data.clear(); st.rerun()


if __name__ == "__main__":
    main()
