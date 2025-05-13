import streamlit as st
import pandas as pd

    
st.title("CONTROLE DE NOTAS :sunglasses:")
sup = ['KATIA', 'DANILO']
supervisor_selecionado = st.selectbox("Selecione o Supervisor:", sup)

Arquivo = "https://docs.google.com/spreadsheets/d/1Lpjc8Zb9_P8vZjt8pjjft66LpGqTE4g7uUy0hlOnUO8/export?format=csv"
df = pd.read_csv(Arquivo)

# Aplica o filtro com base no supervisor selecionado
df_filtrado = df[df['GESTOR_RESP'] == supervisor_selecionado]

st.title("Dados Filtrados por Supervisor")
edited_df = st.data_editor(df_filtrado)

if st.button("Salvar Alterações"):
    try:
        edited_df.to_csv(Arquivo, index=False)
        st.success("As alterações foram salvas com sucesso!")
    except Exception as e:
        st.error(f"Ocorreu um erro ao salvar as alterações: {e}")