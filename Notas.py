import streamlit as st
import pandas as pd

# Carrega o DataFrame
df = pd.read_csv("Notas.csv", sep=";")

# Exibe o editor de dados
edited_df = st.data_editor(df)

# Adiciona um botão para salvar as alterações
if st.button("Salvar Alterações"):
    try:
        edited_df.to_csv("Notas.csv", sep=";", index=False)
        st.success("As alterações foram salvas com sucesso!")
    except Exception as e:
        st.error(f"Ocorreu um erro ao salvar as alterações: {e}")