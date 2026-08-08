import streamlit as st


def apply_theme() -> None:
    dark = bool(st.session_state.get("dark_mode", False))
    colors = {
        "bg": "#0B1220" if dark else "#F4F7FB",
        "surface": "#111B2E" if dark else "#FFFFFF",
        "surface_alt": "#17233A" if dark else "#EEF3FA",
        "text": "#F1F5F9" if dark else "#172033",
        "muted": "#9AA9C0" if dark else "#64748B",
        "border": "#283852" if dark else "#DCE4EF",
        "primary": "#60A5FA" if dark else "#2563EB",
        "sidebar": "#0A1020" if dark else "#EAF0F8",
    }
    st.markdown(
        f"""
        <style>
        :root {{ color-scheme: {'dark' if dark else 'light'}; }}
        .stApp {{ background: {colors['bg']}; color: {colors['text']}; }}
        [data-testid="stHeader"] {{ background: transparent; }}
        [data-testid="stSidebar"] {{
            background: {colors['sidebar']};
            border-right: 1px solid {colors['border']};
        }}
        [data-testid="stSidebar"] hr {{ border-color: {colors['border']}; }}
        [data-testid="stSidebar"] [role="radiogroup"] label {{
            border-radius: 12px; padding: .58rem .7rem; margin-bottom: .2rem;
            transition: background .16s ease, transform .16s ease;
        }}
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
            background: {colors['surface_alt']}; transform: translateX(2px);
        }}
        .block-container {{ max-width: 1180px; padding-top: 2.2rem; padding-bottom: 3rem; }}
        h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] {{ color: {colors['text']}; }}
        .edutrack-hero {{
            padding: 2rem 2.2rem;
            border-radius: 24px;
            background: linear-gradient(135deg, #1D4ED8, #2563EB 55%, #38BDF8);
            box-shadow: 0 22px 55px rgba(37, 99, 235, .22);
            color: white;
            margin-bottom: 1.25rem;
        }}
        .edutrack-hero h1, .edutrack-hero p {{ color: white !important; margin: 0; }}
        .edutrack-hero h1 {{ font-size: clamp(2rem, 4vw, 3.2rem); line-height: 1.08; }}
        .edutrack-hero p {{ margin-top: .8rem; opacity: .9; font-size: 1.05rem; max-width: 620px; }}
        .edutrack-brand {{ font-weight: 800; letter-spacing: -.03em; font-size: 1.35rem; }}
        div[data-testid="stForm"], div[data-testid="stMetric"],
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 18px;
        }}
        div[data-testid="stMetric"] {{ padding: 1rem 1.1rem; box-shadow: 0 8px 24px rgba(15, 23, 42, .06); }}
        div[data-testid="stMetricLabel"] p {{ color: {colors['muted']} !important; }}
        div[data-testid="stMetricValue"] {{ color: {colors['text']}; }}
        .stButton > button, .stDownloadButton > button {{
            border-radius: 12px; min-height: 2.65rem; font-weight: 700;
            border: 1px solid {colors['border']}; transition: .16s ease;
        }}
        .stButton > button[kind="primary"], .stFormSubmitButton > button {{
            background: #2563EB; color: white; border-color: #2563EB;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{ transform: translateY(-1px); }}
        div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {{
            background: {colors['surface_alt']}; border-color: {colors['border']};
        }}
        [data-testid="stDataFrame"] {{ border: 1px solid {colors['border']}; border-radius: 14px; overflow: hidden; }}
        .edutrack-eyebrow {{ color: {colors['primary']}; font-weight: 800; text-transform: uppercase; letter-spacing: .08em; font-size: .75rem; }}
        .edutrack-muted {{ color: {colors['muted']} !important; }}
        @media (max-width: 640px) {{
            .block-container {{ padding: 1rem .9rem 2rem; }}
            .edutrack-hero {{ padding: 1.5rem; border-radius: 18px; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def theme_toggle(*, sidebar: bool = False) -> None:
    target = st.sidebar if sidebar else st
    target.toggle("Modo escuro", key="dark_mode", help="Alternar entre tema claro e escuro")
