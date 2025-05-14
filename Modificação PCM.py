import streamlit as st
import pandas as pd

def check_password():
    """Retorna True se a senha inserida estiver correta e armazena o nome de usuário."""
    def password_entered():
        """Verifica se a senha está correta e atualiza o estado de login."""
        if st.session_state["username"] == "PCM" and \
           st.session_state["password"] ==  "pcm":
            st.session_state["password_correct"] = True
            st.session_state["logged_in_user"] =  "PCM"  # Armazena o nome de usuário
            del st.session_state["password"]  # Não armazene a senha na sessão
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        usernames = "PCM"
        st.title("Login :closed_lock_with_key:")
        username = st.selectbox("Selecione seu nome de usuário:", usernames, key="username")
        password = st.text_input("Senha:", type="password", on_change=password_entered, key="password")
        if st.session_state["password_correct"] is False:
            st.error("Senha incorreta para o usuário selecionado")
        return False
    else:
        return True

if check_password():
    st.title("CONTROLE DE NOTAS :lower_left_fountain_pen:")
    st.button("Refresh")
    logged_in_user = st.session_state.get("logged_in_user")
    Arquivo = "Notas.csv"
    df = pd.read_csv(Arquivo)

    if logged_in_user:

        st.subheader(f"Dados de {logged_in_user}")
        edited_df = st.data_editor(df,num_rows='dynamic')

        if st.button("Salvar Alterações"):
            try:

                edited_df.to_csv(Arquivo)
                st.success("As alterações foram salvas com sucesso!")
            except Exception as e:
                st.error(f"Ocorreu um erro ao salvar as alterações: {e}")
    else:
        st.warning("Nome de usuário não encontrado após o login.")