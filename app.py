import streamlit as st 
import altair as alt 
import pandas as pd 


st.title("Bienvenido a mi aplicación principal")
st.write("Haz clic en los botones de abajo para ir a otras páginas.")

# Botón para ir a la página 1
if st.button("Pagina facturacion maquila"):
    st.switch_page("pages/facturacion_maquila.py")
if st.button("pagina produccion"):
    st.switch_page("pages/produccion.py")
