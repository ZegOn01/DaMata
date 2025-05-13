import streamlit as st
import pandas as pd

def check_password():
    """Retorna True se a senha inserida estiver correta e armazena o nome de usuário."""
    def password_entered():
        """Verifica se a senha está correta e atualiza o estado de login."""
        if st.session_state["username"] in st.secrets["users"] and \
           st.session_state["password"] == st.secrets["users"][st.session_state["username"]]:
            st.session_state["password_correct"] = True
            st.session_state["logged_in_user"] = st.session_state["username"]  # Armazena o nome de usuário
            del st.session_state["password"]  # Não armazene a senha na sessão
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        usernames = list(st.secrets["users"].keys())
        st.title("Login :smile_cat:")
        username = st.selectbox("Selecione seu nome de usuário:", usernames, key="username")
        password = st.text_input("Senha:", type="password", on_change=password_entered, key="password")
        if st.session_state["password_correct"] is False:
            st.error("Senha incorreta para o usuário selecionado")
        return False
    else:
        return True

if check_password():
    st.title("CONTROLE DE NOTAS :sunglasses:")

    # Recupera o nome de usuário logado
    logged_in_user = st.session_state.get("logged_in_user")

    Arquivo = "https://docs.google.com/spreadsheets/d/1Lpjc8Zb9_P8vZjt8pjjft66LpGqTE4g7uUy0hlOnUO8/export?format=csv"
    df = pd.read_csv(Arquivo)

    if logged_in_user:
        # Filtra o DataFrame com base no usuário logado (assumindo que há uma coluna 'Responsável' ou similar)
        # Adapte o nome da coluna ('Responsável') para o nome correto na sua planilha.
        coluna_responsavel = 'GESTOR_RESP'  # Substitua pelo nome da sua coluna de responsável
        df_filtrado = df[df[coluna_responsavel] == logged_in_user]
        st.subheader(f"Dados de {logged_in_user}")
        edited_df = st.data_editor(df_filtrado)

        if st.button("Salvar Alterações"):
            try:
                # Aqui, a lógica de salvamento precisa considerar que você está editando uma parte filtrada dos dados.
                # Uma abordagem simples (mas potencialmente com os problemas mencionados anteriormente) é salvar o edited_df de volta.
                edited_df.to_csv(Arquivo, index=False)
                st.success("As alterações foram salvas com sucesso!")
            except Exception as e:
                st.error(f"Ocorreu um erro ao salvar as alterações: {e}")
    else:
        st.warning("Nome de usuário não encontrado após o login.")