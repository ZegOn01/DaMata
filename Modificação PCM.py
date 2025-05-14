import streamlit as st
import pandas as pd
from datetime import datetime
import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1z8ivbjByKSOd3xxGjrP82KArY_FkGByoat0fu0_rZ0I"


def Get_Tabela():
    """Shows basic usage of the Sheets API and returns a Pandas DataFrame."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "ClienteSecret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Notas")
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return None  # Retorna None se não houver dados
        else:
            header = values[0]
            data = values[1:]
            df = pd.DataFrame(data, columns=header)
            return df  # Retorna o DataFrame criado

    except HttpError as err:
        print(err)
        return None  # Retorna None em caso de erro


def update_tabela(df_atualizado):
    """Atualiza os dados na planilha do Google Sheets com os dados do DataFrame."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "ClienteSecret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Formata os dados do DataFrame para o formato esperado pela API do Sheets
        data = [df_atualizado.columns.tolist()] + df_atualizado.values.tolist()
        body = {"values": data}

        result = (
            sheet.values()
            .update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range="Notas",  # Mesma aba que você leu ("Notas")
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} células atualizadas.")
        return True  # Indica que a atualização foi bem-sucedida

    except HttpError as error:
        print(f"Ocorreu um erro: {error}")
        return False # Indica que a atualização falhou

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
    df = Get_Tabela() 
    df['ASSINATURA'] = df['ASSINATURA'].replace({'FALSE': False, 'TRUE': True})

    if logged_in_user:

        st.subheader(f"Dados de {logged_in_user}")
        edited_df = st.data_editor(df,num_rows='dynamic')

        if st.button("Salvar Alterações"):
            try:

                update_tabela(df)
                st.success("As alterações foram salvas com sucesso!")
            except Exception as e:
                st.error(f"Ocorreu um erro ao salvar as alterações: {e}")
    else:
        st.warning("Nome de usuário não encontrado após o login.")