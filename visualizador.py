import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de conexión a PostgreSQL
conexion = psycopg2.connect(
    dbname="dpanchita2",
    user="postgres",
    password="123456",
    host="localhost",  # o la IP de tu servidor
    port="5432"        # Puerto por defecto de PostgreSQL
)

# Función para obtener datos de la base de datos
def obtener_datos(query):
    return pd.read_sql(query, conexion)


# Consulta para obtener el total de ventas por mes
query_ventas_mes = '''
    SELECT d.mes, SUM(hv.total) AS total_ventas
    FROM Hechos_Ventas hv
    JOIN Dim_Fecha d ON hv.id_fecha = d.id_fecha
    GROUP BY d.mes
    ORDER BY d.mes
'''

df_ventas_mes = obtener_datos(query_ventas_mes)

# Título de la aplicación
st.title('Reportes de Ventas - Doña Panchita')

# Menú lateral para seleccionar el reporte
opciones = ['Univariados', 'Bivariados']
reporte_seleccionado = st.sidebar.selectbox('Selecciona el reporte', opciones)

if reporte_seleccionado == 'Univariados':
    st.header('Reportes Univariados')

    # Reporte: Distribución de Ventas por Sucursal
    sucursales = obtener_datos(''' 
        SELECT s.nombre, COUNT(hv.id_venta) AS total_ventas
        FROM Hechos_Ventas hv
        JOIN Dim_Sucursales s ON hv.id_sucursal = s.id_sucursal
        GROUP BY s.nombre
    ''')
    st.subheader('Distribución de Ventas por Sucursal')
    grafico_sucursales = st.selectbox('Selecciona el tipo de gráfico', ['Barra', 'Pastel'])
    if grafico_sucursales == 'Barra':
        # Gráfico de barra interactivo
        fig = px.bar(sucursales, x='nombre', y='total_ventas', title='Ventas por Sucursal', 
                     labels={'nombre': 'Sucursal', 'total_ventas': 'Total de Ventas'}, 
                     text='total_ventas')
        fig.update_traces(texttemplate='%{text}', textposition='outside', hoverinfo='x+y')
        st.plotly_chart(fig)
    else:
        # Gráfico de pastel interactivo
        # Crear gráfico de pastel
        fig = px.pie(sucursales, names='nombre', values='total_ventas', title='Distribución de Ventas por Sucursal')
        # Actualizar el gráfico para agregar texto con etiquetas y porcentajes
        fig.update_traces(textinfo='label+percent', pull=[0.1, 0.1, 0.1])  # Personalizar el texto

        st.plotly_chart(fig)

    # Reporte: Cantidad de Ventas por Categoría y Subcategoría de Producto
    categorias = obtener_datos(''' 
        SELECT c.nombre AS categoria, sc.nombre_subcategoria, COUNT(hv.id_venta) AS total_ventas
        FROM Hechos_Ventas hv
        JOIN Dim_Productos p ON hv.id_producto = p.id_producto
        JOIN Dim_Subcategorias sc ON p.id_subcategoria = sc.id_subcategoria
        JOIN Dim_Categorias c ON sc.id_categoria = c.id_categoria
        GROUP BY c.nombre, sc.nombre_subcategoria
        ORDER BY total_ventas DESC
    ''')
    st.subheader('Cantidad de Ventas por Categoría y Subcategoría')
    grafico_categorias = st.selectbox('Selecciona el tipo de gráfico', ['Barra'])
    if grafico_categorias == 'Barra':
        # Gráfico de barras interactivo
        fig = px.bar(categorias, x='total_ventas', y='categoria', color='nombre_subcategoria', 
                     title='Ventas por Categoría y Subcategoría', 
                     labels={'categoria': 'Categoría', 'total_ventas': 'Total de Ventas'}, 
                     text='total_ventas', orientation='h')
        fig.update_traces(texttemplate='%{text}', textposition='outside', hoverinfo='x+y')
        st.plotly_chart(fig)

    # Reporte: Distribución de Clientes por Género
    # Obtener datos de género
    generos = obtener_datos(''' 
        SELECT g.genero, COUNT(c.id_cliente) AS total_clientes
        FROM Dim_Clientes c
        JOIN Dim_Genero g ON c.id_genero = g.id_genero
        GROUP BY g.genero
    ''')

    # Título de la sección
    st.subheader('Distribución de Clientes por Género')

    # Selección de tipo de gráfico
    grafico_genero = st.selectbox('Selecciona el tipo de gráfico', ['Pie chart'])

    # Si elige "Pie chart"
    if grafico_genero == 'Pie chart':
        # Crear el gráfico de pastel
        fig = px.pie(generos, names='genero', values='total_clientes', 
                    title='Distribución de Clientes por Género')
        
        # Configurar el texto y la información del hover
        fig.update_traces(textinfo='label+percent', hoverinfo='label+percent+value')

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)

    # Reporte: Métodos de Pago Utilizados
    # Obtener datos de métodos de pago
    metodos_pago = obtener_datos(''' 
        SELECT mp.metodo_pago, COUNT(hv.id_venta) AS total_ventas
        FROM Hechos_Ventas hv
        JOIN Dim_Metodos_Pago mp ON hv.id_metodo_pago = mp.id_metodo_pago
        GROUP BY mp.metodo_pago
    ''')

    # Título de la sección
    st.subheader('Métodos de Pago Utilizados')

    # Selección de tipo de gráfico
    grafico_metodos_pago = st.selectbox('Selecciona el tipo de gráfico', ['Pie chart', 'Barra'])

    # Si elige "Pie chart"
    if grafico_metodos_pago == 'Pie chart':
        # Crear el gráfico de pastel
        fig = px.pie(metodos_pago, names='metodo_pago', values='total_ventas', 
                    title='Métodos de Pago Utilizados')
        
        # Configurar el texto y la información del hover
        fig.update_traces(textinfo='label+percent', hoverinfo='label+percent+value')

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)

    # Si elige "Barra"
    else:
        # Crear el gráfico de barras
        fig = px.bar(metodos_pago, x='metodo_pago', y='total_ventas', 
                    title='Métodos de Pago Utilizados', 
                    labels={'metodo_pago': 'Método de Pago', 'total_ventas': 'Total de Ventas'}, 
                    text='total_ventas')
        
        # Configurar el texto de las barras y la información del hover
        fig.update_traces(texttemplate='%{text}', textposition='outside', hoverinfo='x+y')

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)
elif reporte_seleccionado == 'Bivariados':
    st.header('Reportes Bivariados')
    #reporte 1
    # Obtener datos de ventas por sucursal y fecha
    ventas_sucursal_fecha = obtener_datos(''' 
        SELECT s.nombre AS sucursal, f.dia_semana, SUM(hv.total) AS total_ventas
        FROM Hechos_Ventas hv
        JOIN Dim_Sucursales s ON hv.id_sucursal = s.id_sucursal
        JOIN Dim_Fecha f ON hv.id_fecha = f.id_fecha
        GROUP BY s.nombre, f.dia_semana
        ORDER BY total_ventas DESC
    ''')

    # Título de la sección
    st.subheader('Total de Ventas por Sucursal y por Fecha')

    # Gráfico de heatmap
    ventas_sucursal_fecha_pivot = ventas_sucursal_fecha.pivot(index='sucursal', columns='dia_semana', values='total_ventas')

    # Crear el gráfico de heatmap
    fig = go.Figure(data=go.Heatmap(z=ventas_sucursal_fecha_pivot.values, 
                                x=ventas_sucursal_fecha_pivot.columns, 
                                y=ventas_sucursal_fecha_pivot.index, 
                                colorscale='Viridis'))

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    # Cantidad de Productos Vendidos por Categoría y por Sucursal
    productos_categorias_sucursales = obtener_datos(''' 
        SELECT c.nombre AS categoria, s.nombre AS sucursal, COUNT(hv.id_venta) AS total_ventas
        FROM Hechos_Ventas hv
        JOIN Dim_Productos p ON hv.id_producto = p.id_producto
        JOIN Dim_Subcategorias sc ON p.id_subcategoria = sc.id_subcategoria
        JOIN Dim_Categorias c ON sc.id_categoria = c.id_categoria
        JOIN Dim_Sucursales s ON hv.id_sucursal = s.id_sucursal
        GROUP BY c.nombre, s.nombre
    ''')
    st.subheader('Cantidad de Productos Vendidos por Categoría y por Sucursal')
    grafico_prod_sucursal = st.selectbox('Selecciona el tipo de gráfico', ['Barra', 'Stacked Barra'])
    if grafico_prod_sucursal == 'Barra':
        # Gráfico de barras interactivo
        fig = px.bar(productos_categorias_sucursales, x='total_ventas', y='categoria', color='sucursal', 
                     title='Productos Vendidos por Categoría y Sucursal', 
                     labels={'categoria': 'Categoría', 'total_ventas': 'Total de Ventas'}, 
                     text='total_ventas', orientation='h')
        fig.update_traces(texttemplate='%{text}', textposition='outside', hoverinfo='x+y')
        st.plotly_chart(fig)
    else:
        # Gráfico de barras apiladas
        fig = px.bar(productos_categorias_sucursales, x='categoria', y='total_ventas', color='sucursal', 
                     title='Productos Vendidos por Categoría y Sucursal', 
                     labels={'categoria': 'Categoría', 'total_ventas': 'Total de Ventas'})
        st.plotly_chart(fig)
