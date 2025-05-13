import streamlit as st
import pandas as pd

df = pd.read_csv("Notas.csv",sep= ";")


st.data_editor(df)
