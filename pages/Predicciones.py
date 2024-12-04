import streamlit as st
import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

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
    query = "SELECT id_sucursal, id_producto, id_cliente, cantidad, total FROM Hechos_Ventas;"
    datos = pd.read_sql(query, conn)
    conn.close()
    return datos

# Mostrar los datos
st.title("Comparación de Modelos Predictivos")
datos = cargar_datos()
st.write("Vista previa de los datos:", datos.head())

# Preparación de datos
st.subheader("Preparación de Datos")
X = datos[['id_sucursal', 'id_producto', 'id_cliente', 'cantidad']]
y = datos['total']

# Dividir datos en entrenamiento y prueba (80%-20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

st.write(f"Datos de entrenamiento: {X_train.shape[0]} filas")
st.write(f"Datos de prueba: {X_test.shape[0]} filas")

# Función para evaluar modelos
def evaluar_modelo(nombre, modelo, X_train, X_test, y_train, y_test):
    modelo.fit(X_train, y_train)
    predicciones = modelo.predict(X_test)
    mae = mean_absolute_error(y_test, predicciones)
    mse = mean_squared_error(y_test, predicciones)
    r2 = r2_score(y_test, predicciones)
    return {
        "Modelo": nombre,
        "MAE": mae,
        "MSE": mse,
        "R²": r2
    }, predicciones

# Entrenar y evaluar modelos
st.subheader("Resultados de los Modelos")
resultados = []

# Modelo 1: Regresión Lineal
modelo_lr = LinearRegression()
resultado_lr, predicciones_lr = evaluar_modelo("Regresión Lineal", modelo_lr, X_train, X_test, y_train, y_test)
resultados.append(resultado_lr)

# Modelo 2: Random Forest
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
resultado_rf, predicciones_rf = evaluar_modelo("Random Forest", modelo_rf, X_train, X_test, y_train, y_test)
resultados.append(resultado_rf)

# Modelo 3: Gradient Boosting
modelo_gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
resultado_gb, predicciones_gb = evaluar_modelo("Gradient Boosting", modelo_gb, X_train, X_test, y_train, y_test)
resultados.append(resultado_gb)

# Modelo 4: XGBoost
modelo_xgb = XGBRegressor(n_estimators=100, random_state=42)
resultado_xgb, predicciones_xgb = evaluar_modelo("XGBoost", modelo_xgb, X_train, X_test, y_train, y_test)
resultados.append(resultado_xgb)

# Mostrar resultados en tabla
df_resultados = pd.DataFrame(resultados)
st.write("Comparación de los Modelos:", df_resultados)

# Visualización: Valores Reales vs Predicciones
st.subheader("Comparación: Valores Reales vs Predicciones")
comparacion = pd.DataFrame({
    "Valores Reales": y_test,
    "Predicciones (RL)": predicciones_lr,
    "Predicciones (RF)": predicciones_rf,
    "Predicciones (GB)": predicciones_gb,
    "Predicciones (XGB)": predicciones_xgb
}).reset_index(drop=True)

# Multi selección de modelos para graficar
modelos_seleccionados = st.multiselect(
    "Selecciona los modelos para graficar:",
    options=["Regresión Lineal", "Random Forest", "Gradient Boosting", "XGBoost"],
    default=["Regresión Lineal"]  # Valor predeterminado
)

# Crear el DataFrame de predicciones con los modelos seleccionados
grafico_comparativo = pd.DataFrame({"Valores Reales": y_test})

# Añadir las predicciones de los modelos seleccionados
if "Regresión Lineal" in modelos_seleccionados:
    grafico_comparativo["Predicciones Regresión Lineal"] = predicciones_lr
if "Random Forest" in modelos_seleccionados:
    grafico_comparativo["Predicciones Random Forest"] = predicciones_rf
if "Gradient Boosting" in modelos_seleccionados:
    grafico_comparativo["Predicciones Gradient Boosting"] = predicciones_gb
if "XGBoost" in modelos_seleccionados:
    grafico_comparativo["Predicciones XGBoost"] = predicciones_xgb

# Mostrar la comparación en tabla
st.write(grafico_comparativo)

# Gráfico comparativo
st.line_chart(grafico_comparativo)
