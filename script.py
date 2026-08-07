import streamlit as st

# 1. Configuração inicial da página
st.set_page_config(page_title="Sistema de Login", page_icon="🔒", layout="centered")

# 2. Inicializa o estado de login se não existir
if "conectado" not in st.session_state:
    st.session_state.conectado = False
if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = ""

# Usuários e senhas de teste (Em produção, use st.secrets ou banco de dados)
CREDENCIAIS_VALIDAS = {
    "admin": "senha123",
    "usuario": "streamlit2026"
}

# Função para validar o login
def efetuar_login(usuario, senha):
    if usuario in CREDENCIAIS_VALIDAS and CREDENCIAIS_VALIDAS[usuario] == senha:
        st.session_state.conectado = True
        st.session_state.usuario_atual = usuario
        st.success(f"👋 Bem-vindo de volta, {usuario}!")
        st.rerun()
    else:
        st.error("❌ Usuário ou senha incorretos.")

# 3. Tela de Login (Exibida se o usuário NÃO estiver conectado)
if not st.session_state.conectado:
    st.title("🔒 Área de Acesso")
    st.write("Insira suas credenciais para acessar o painel.")

    # Criação do formulário de login
    with st.form(key="formulario_login"):
        input_usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
        input_senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        botao_enviar = st.form_submit_button(label="Entrar", use_container_width=True)

    # Processa os dados quando o botão é clicado
    if botao_enviar:
        if input_usuario and input_senha:
            efetuar_login(input_usuario, input_senha)
        else:
            st.warning("⚠️ Por favor, preencha todos os campos.")

# 4. Conteúdo Protegido (Exibido APENAS se o usuário estiver conectado)
else:
    # Barra lateral com botão de Logout
    with st.sidebar:
        st.write(f"Conectado como: **{st.session_state.usuario_atual}**")
        if st.button("Sair / Logout", use_container_width=True):
            st.session_state.conectado = False
            st.session_state.usuario_atual = ""
            st.rerun()

    # Conteúdo principal do seu aplicativo
    st.title("📊 Painel de Controle Protegido")
    st.write("Parabéns! Você acessou a área segura do aplicativo.")
    st.info("Todo o código executado nesta seção está protegido pelo sistema de login.")
    
    # Exemplo de funcionalidade do app
    st.metric(label="Vendas Totais", value="R$ 45.230,00", delta="+12%")
