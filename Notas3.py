import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Função para carregar os dados (agora com tratamento de cache)
@st.cache_data
def carregar_dados():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "DATA.csv")
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error("O arquivo DATA.csv não foi encontrado.")
        st.stop()

# Carrega os dados usando a função cacheada
if 'documentos' not in st.session_state:
    st.session_state['documentos'] = carregar_dados()

documentos = st.session_state['documentos']

# Garante que a coluna 'Data_Assinatura' seja do tipo datetime
documentos['Data_Assinatura'] = pd.to_datetime(documentos['Data_Assinatura'], errors='coerce')

st.title("Assinatura de Documentos")

st.write("Selecione os documentos para assinar:")
documentos_selecionados = st.data_editor(documentos.copy(), num_rows="dynamic", key="data_editor") # Adicionamos uma key ao data_editor

if st.button("Selecionar Documentos para Assinar"):
    documentos_para_assinar = documentos_selecionados[(documentos_selecionados['Assinatura'] == True) & (documentos_selecionados['Data_Assinatura'].isna())].copy()
    if not documentos_para_assinar.empty:
        st.text('Documentos que serão assinados:')
        documentos_para_assinar['Data_Assinatura'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        st.dataframe(documentos_para_assinar)

        if st.button("Confirmar Assinatura"):
            try:
                for index, row in documentos_para_assinar.iterrows():
                    st.session_state['documentos'].loc[st.session_state['documentos']['Documentos'] == row['Documentos'], 'Data_Assinatura'] = row['Data_Assinatura']
                    st.session_state['documentos'].loc[st.session_state['documentos']['Documentos'] == row['Documentos'], 'Assinatura'] = True

                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, "DATA.csv")
                st.session_state['documentos'].to_csv(csv_path, index=False)
                st.success("Documentos assinados e arquivo atualizado com sucesso!")

                # Atualiza a exibição do data_editor
                st.session_state['documentos'] = pd.read_csv(csv_path) # Recarrega os dados
                st.experimental_rerun() # Força uma reexecução do script para atualizar a interface
            except Exception as e:
                st.error(f"Ocorreu um erro ao salvar o arquivo: {e}")
    else:
        st.warning("Nenhum documento selecionado para assinatura.")