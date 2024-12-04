import streamlit as st
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import numpy as np

# Configurar la página
st.set_page_config(layout="wide")

# Título de la aplicación
st.title("Análisis de Componentes Principales (PCA) con Streamlit y Plotly")

# Cargar el dataset externo
st.header("1. Cargar dataset")

# Subida de archivo
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xls", "xlsx"])

if uploaded_file is not None:
    @st.cache_data
    def load_data(file):
        # Lee el archivo Excel
        df = pd.read_excel(file)
        return df

    df = load_data(uploaded_file)
    st.write("### Dataset original:")
    st.dataframe(df.head())

    # Seleccionar las variables para PCA (variables numéricas)
    st.header("2. Selección de variables para PCA")
    selected_columns = st.multiselect("Selecciona las variables para el PCA", df.columns.tolist(), default=df.columns[:4].tolist())
    st.write("Variables seleccionadas:", selected_columns)

    # Continuar con el análisis
    if selected_columns:
        # Estandarización de los datos
        st.header("3. Estandarización de los datos")
        st.write("El PCA requiere que las variables estén estandarizadas para que todas tengan la misma importancia.")
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df[selected_columns])

        st.write("### Datos escalados (primeras 5 filas):")
        st.dataframe(pd.DataFrame(scaled_data, columns=selected_columns).head())

        # Calcular la matriz de covarianza
        st.header("4. Matriz de Covarianza")
        cov_matrix = np.cov(scaled_data, rowvar=False)
        st.write("### Matriz de Covarianza:")
        st.dataframe(pd.DataFrame(cov_matrix, columns=selected_columns, index=selected_columns))

        # Aplicar PCA
        st.header("5. Aplicación de PCA")
        n_components = st.slider("Número de componentes", min_value=1, max_value=len(selected_columns), value=2)
        pca = PCA(n_components=n_components)
        pca_result = pca.fit_transform(scaled_data)

        # Obtener los vectores propios
        st.header("6. Vectores propios (Eigenvectors)")
        eigenvectors = pca.components_
        st.dataframe(pd.DataFrame(eigenvectors, columns=selected_columns, index=[f'PC{i+1}' for i in range(n_components)]))

        # Crear un DataFrame con los resultados del PCA
        pca_df = pd.DataFrame(pca_result, columns=[f'PC{i+1}' for i in range(n_components)])
        st.write(f"### Resultado del PCA con {n_components} componentes principales:")
        st.dataframe(pca_df.head())

        # Explicación de la varianza acumulada
        explained_variance = pca.explained_variance_ratio_
        
        # Gráfico de barras de varianza explicada
        st.header("8. Varianza Explicada por cada Componente")
        fig_bar = px.bar(
            x=[f'PC{i+1}' for i in range(n_components)],
            y=explained_variance,
            labels={'x': 'Componente Principal', 'y': 'Varianza Explicada (%)'},
            title="Varianza Explicada por cada Componente Principal",
            color=[f'PC{i+1}' for i in range(n_components)],
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        st.plotly_chart(fig_bar)

        total_variance = sum(explained_variance)
        st.write(f"### Varianza total explicada: {total_variance:.2f}")

        # Visualización de los Componentes Principales
        st.header("7. Visualización de los Componentes Principales")
        if 'Categoría' not in pca_df.columns:
            pca_df['Categoría'] = np.random.choice(['Grupo A', 'Grupo B', 'Grupo C'], size=len(pca_df))

        if n_components < 3:
            st.write("Gráfico interactivo de los dos primeros componentes principales.")
            fig = px.scatter(
                pca_df, x='PC1', y='PC2', color='Categoría',
                title="Gráfico de los dos primeros Componentes Principales",
                color_discrete_sequence=px.colors.qualitative.Bold,
                labels={
                    'PC1': f'PC1 ({explained_variance[0]:.2%} varianza explicada)',
                    'PC2': f'PC2 ({explained_variance[1]:.2%} varianza explicada)'
                }
            )
            st.plotly_chart(fig)
        elif n_components >= 3:
            st.write("Gráfico interactivo 3D de los tres primeros componentes principales.")
            fig_3d = px.scatter_3d(
                pca_df, x='PC1', y='PC2', z='PC3', color='Categoría',
                title="Gráfico 3D de los tres primeros Componentes Principales",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                labels={
                    'PC1': f'PC1 ({explained_variance[0]:.2%} varianza explicada)',
                    'PC2': f'PC2 ({explained_variance[1]:.2%} varianza explicada)',
                    'PC3': f'PC3 ({explained_variance[2]:.2%} varianza explicada)'
                }
            )
            st.plotly_chart(fig_3d)
else:
    st.write("Por favor, sube un archivo para continuar.")