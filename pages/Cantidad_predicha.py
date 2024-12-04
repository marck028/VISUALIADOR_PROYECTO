import streamlit as st
import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import plotly.express as px

# Conexión a PostgreSQL
@st.cache_resource
def conectar_base_datos():
    return psycopg2.connect(
        dbname="dpanchita2",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )

# Cargar datos de PostgreSQL
@st.cache_data
def cargar_datos():
    conn = conectar_base_datos()
    query = "SELECT id_sucursal, id_producto, fecha, cantidad FROM Hechos_Ventas;"
    datos = pd.read_sql(query, conn)
    conn.close()
    return datos

# Mostrar los datos
st.title("Predicción de Cantidad de Productos Vendidos")
datos = cargar_datos()
st.write("Vista previa de los datos:", datos.head())

# Preprocesamiento de los datos
st.subheader("Preparación de los Datos")
# Convertir la fecha a formato datetime
datos['fecha'] = pd.to_datetime(datos['fecha'])
# Extraer características útiles de la fecha
datos['año'] = datos['fecha'].dt.year
datos['mes'] = datos['fecha'].dt.month
datos['día'] = datos['fecha'].dt.day
datos['día_semana'] = datos['fecha'].dt.weekday  # Lunes=0, Domingo=6

# Selección de características (X) y variable objetivo (y)
X = datos[['id_sucursal', 'id_producto', 'año', 'mes', 'día', 'día_semana']]
y = datos['cantidad']

# Dividir los datos en conjunto de entrenamiento y prueba (80%-20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

st.write(f"Datos de entrenamiento: {X_train.shape[0]} filas")
st.write(f"Datos de prueba: {X_test.shape[0]} filas")

# Entrenar el modelo: Random Forest
st.subheader("Entrenando el Modelo")
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_rf.fit(X_train, y_train)

# Predicciones
predicciones_rf = modelo_rf.predict(X_test)

# Evaluación del modelo
mae = mean_absolute_error(y_test, predicciones_rf)
mse = mean_squared_error(y_test, predicciones_rf)
r2 = r2_score(y_test, predicciones_rf)

st.write("Resultados del Modelo:")
st.write(f"MAE (Error Absoluto Medio): {mae}")
st.write(f"MSE (Error Cuadrático Medio): {mse}")
st.write(f"R² (Coeficiente de Determinación): {r2}")

# Visualización: Predicciones vs Valores Reales
st.subheader("Comparación: Predicciones vs Valores Reales")
comparacion = pd.DataFrame({
    "Valores Reales": y_test,
    "Predicciones": predicciones_rf
}).reset_index(drop=True)

# Gráfico interactivo de predicciones vs reales
fig = px.scatter(comparacion, 
                 x=comparacion.index, 
                 y=["Valores Reales", "Predicciones"], 
                 labels={"index": "Índice", "value": "Cantidad", "variable": "Tipo de Valor"},
                 title="Comparación de Cantidades Reales vs Predicciones",
                 color_discrete_sequence=["blue", "red"])

# Mostrar gráfico
st.plotly_chart(fig)

# Predicción interactiva
st.subheader("Predicción Interactiva")
sucursal_input = st.selectbox("Selecciona una Sucursal", options=datos['id_sucursal'].unique())
producto_input = st.selectbox("Selecciona un Producto", options=datos['id_producto'].unique())
fecha_input = st.date_input("Selecciona la Fecha", value=pd.to_datetime("2024-12-01"))

# Convertir la fecha seleccionada a características numéricas
fecha_input = pd.to_datetime(fecha_input)
año_input = fecha_input.year
mes_input = fecha_input.month
día_input = fecha_input.day
día_semana_input = fecha_input.weekday()

# Crear el DataFrame para la predicción
entrada = pd.DataFrame({
    'id_sucursal': [sucursal_input],
    'id_producto': [producto_input],
    'año': [año_input],
    'mes': [mes_input],
    'día': [día_input],
    'día_semana': [día_semana_input]
})

# Realizar la predicción
prediccion_cantidad = modelo_rf.predict(entrada)

st.write(f"La predicción de la cantidad de productos vendidos es: {prediccion_cantidad[0]:.2f}")
