import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar los datos
@st.cache
def load_data(file_path):
    return pd.read_excel(file_path)

# Título de la aplicación
st.title("EDA para Doña Panchita")

# Cargar el archivo de Excel
file_path = "C:/Users/Marco/Documents/UNIVERSIDAD/4 SEMESTRE/PROYECTO INTEGRADOR/VISUALIADOR_PROYECTO/data_tabla_hechos.xls"
df = load_data(file_path)

# Mostrar los primeros registros
st.subheader("Primeros registros del dataset")
st.write(df.head())

# Mostrar información básica
st.subheader("Información del dataset")
st.write(df.info())

# Mostrar estadísticas descriptivas
st.subheader("Estadísticas descriptivas")
st.write(df.describe())

# Visualización de gráficos
st.subheader("Visualizaciones")

# Histograma
st.write("Histograma de una columna seleccionada")
column = st.selectbox("Selecciona una columna para el histograma", df.select_dtypes(include=['float64', 'int64']).columns)
fig, ax = plt.subplots()
sns.histplot(df[column], kde=True, ax=ax)
st.pyplot(fig)

# Mapa de calor de correlación
st.subheader("Mapa de calor de correlación (Selecciona columnas)")
selected_columns = st.multiselect(
    "Selecciona las columnas para el mapa de calor",
    df.select_dtypes(include=['float64', 'int64']).columns
)

if selected_columns:
    corr = df[selected_columns].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
else:
    st.write("Selecciona al menos una columna para generar el mapa de calor.")

# Gráfico de dispersión
st.subheader("Gráfico de dispersión")
col1, col2 = st.columns(2)
x_axis = col1.selectbox("Selecciona el eje X", df.columns)
y_axis = col2.selectbox("Selecciona el eje Y", df.columns)

fig, ax = plt.subplots()
sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
st.pyplot(fig)