import streamlit as st
import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import plotly.express as px
import random

# Conexión a PostgreSQL sin usar caché
def conectar_base_datos():
    try:
        conn = psycopg2.connect(
            dbname="dpanchita2",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        st.error(f"Error al conectar a la base de datos: {e}")
        return None

# Cargar datos de PostgreSQL
def cargar_datos():
    conn = conectar_base_datos()
    if conn is None:
        return pd.DataFrame()  # Si la conexión falla, devolver un DataFrame vacío
    try:
        query = """
        SELECT id_sucursal, id_producto, id_fecha, cantidad, id_fecha::date as fecha 
        FROM Hechos_Ventas;
        """
        datos = pd.read_sql(query, conn)
        return datos
    except Exception as e:
        st.error(f"Error al ejecutar la consulta: {e}")
        return pd.DataFrame()  # En caso de error en la consulta, devolver un DataFrame vacío
    finally:
        conn.close()  # Asegurarse de cerrar la conexión después de la consulta

# Mostrar los datos
st.title("Predicción de Cantidad de Productos Vendidos")
datos = cargar_datos()
if datos.empty:
    st.warning("No se pudieron cargar los datos.")
else:
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

# Modelos disponibles
modelos = {
    "Regresión Lineal": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "XGBoost": xgb.XGBRegressor(random_state=42)
}

# Entrenar todos los modelos
resultados_modelos = {}
for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    predicciones = modelo.predict(X_test)
    mae = mean_absolute_error(y_test, predicciones)
    mse = mean_squared_error(y_test, predicciones)
    r2 = r2_score(y_test, predicciones)
    resultados_modelos[nombre] = {
        "modelo": modelo,
        "predicciones": predicciones,
        "mae": mae,
        "mse": mse,
        "r2": r2
    }

# Mostrar resultados de todos los modelos
st.subheader("Resultados de los Modelos")
for nombre, resultado in resultados_modelos.items():
    st.write(f"Modelo: {nombre}")
    st.write(f"MAE: {resultado['mae']:.2f}")
    st.write(f"MSE: {resultado['mse']:.2f}")
    st.write(f"R²: {resultado['r2']:.2f}")
    st.write("---")

# Selección de modelos a comparar
st.subheader("Selecciona los Modelos para Comparar")
modelos_seleccionados = st.multiselect(
    "Selecciona los modelos que deseas comparar con los valores reales",
    options=list(resultados_modelos.keys()),
    default=list(resultados_modelos.keys())  # Todos los modelos seleccionados por defecto
)

# Crear el DataFrame de comparación
comparacion = pd.DataFrame({
    "Valores Reales": y_test
}).reset_index(drop=True)

# Agregar las predicciones de los modelos seleccionados al DataFrame
for modelo_seleccionado in modelos_seleccionados:
    comparacion[modelo_seleccionado] = resultados_modelos[modelo_seleccionado]["predicciones"]

# Asignar colores únicos para cada modelo seleccionado
colores = ["blue", "red", "green", "purple", "orange", "brown", "pink", "cyan"]
colores_modelos = {modelo: random.choice(colores) for modelo in modelos_seleccionados}

# Gráfico interactivo de puntos (scatter plot)
fig = px.scatter(comparacion, 
                 x=comparacion.index, 
                 y="Valores Reales", 
                 labels={"index": "Índice", "Valores Reales": "Cantidad"},
                 title="Comparación de Cantidades Reales vs Predicciones", 
                 template="plotly_dark")

# Agregar las predicciones al gráfico con colores únicos
for modelo_seleccionado in modelos_seleccionados:
    fig.add_scatter(x=comparacion.index, 
                    y=comparacion[modelo_seleccionado], 
                    mode="markers", 
                    name=f"Predicciones {modelo_seleccionado}", 
                    marker=dict(color=colores_modelos[modelo_seleccionado]))

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

# Realizar la predicción con cada modelo seleccionado
for nombre, resultado in resultados_modelos.items():
    prediccion_cantidad = resultado["modelo"].predict(entrada)
    st.write(f"Predicción con {nombre}: {prediccion_cantidad[0]:.2f}")



