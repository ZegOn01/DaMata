import streamlit as st
import pandas as pd
from datetime import datetime

def check_password():
    def password_entered():
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

        coluna_responsavel = 'GESTOR_RESP'  # Substitua pelo nome da sua coluna de responsável
        df_filtrado = df[df[coluna_responsavel] == logged_in_user]
        st.subheader(f"Dados de {logged_in_user}")
        edited_df = st.data_editor(df_filtrado,disabled=("NF", "FORNECEDOR","VALOR","DT VENC", "GESTOR_RESP","GESTORASSINATURA"))

        if st.button("Salvar Alterações"):
            try:
                edited_df.loc[df['ENTREGA'] == True & df['GESTORASSINATURA'].isna(), 'GESTORASSINATURA'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                df.loc[df['GESTOR_RESP'] == logged_in_user] = edited_df
                df.to_csv(Arquivo, index=False)
                st.success("As alterações foram salvas com sucesso!")
            except Exception as e:
                st.error(f"Ocorreu um erro ao salvar as alterações: {e}")
    else:
        st.warning("Nome de usuário não encontrado após o login.")