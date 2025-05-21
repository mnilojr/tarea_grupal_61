import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar el estilo de los gráficos
sns.set_style("whitegrid")

# Cargar los datos
@st.cache_data
def load_data():
    # Asegúrate de que el archivo CSV esté en el mismo directorio que tu script o proporciona la ruta completa.
    # Si estás en Google Colab, la carga de archivos es diferente a un script local.
    # Para este ejemplo de script local, asumimos que el archivo está presente.
    try:
        df = pd.read_csv('data trabajo grupal visualizacion.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        st.error("Error: Archivo 'data trabajo grupal visualizacion.csv' no encontrado.")
        st.stop()


ventas = load_data()

# Título del Dashboard
st.title("Dashboard de Análisis de Ventas de Tienda de Conveniencia")

# --- Widgets para filtrar datos ---

st.sidebar.header("Filtros")

# Selector de Sucursal
sucursales = ventas['Branch'].unique().tolist()
sucursales_seleccionadas = st.sidebar.multiselect(
    "Selecciona Sucursal:",
    sucursales,
    default=sucursales
)

# Selector de Género
generos = ventas['Gender'].unique().tolist()
generos_seleccionados = st.sidebar.multiselect(
    "Selecciona Género:",
    generos,
    default=generos
)

# Selector de Tipo de Pago
tipos_pago = ventas['Payment'].unique().tolist()
tipos_pago_seleccionados = st.sidebar.multiselect(
    "Selecciona Tipo de Pago:",
    tipos_pago,
    default=tipos_pago
)

# Selector de Línea de Producto
lineas_producto = ventas['Product line'].unique().tolist()
lineas_producto_seleccionadas = st.sidebar.multiselect(
    "Selecciona Línea de Producto:",
    lineas_producto,
    default=lineas_producto
)

# Selector de Rango de Valor Total
min_total = float(ventas['Total'].min())
max_total = float(ventas['Total'].max())
rango_total_seleccionado = st.sidebar.slider(
    "Selecciona Rango de Valor Total:",
    min_total,
    max_total,
    (min_total, max_total)
)

# Selector de Rango de Fechas
min_date = ventas['Date'].min().date()
max_date = ventas['Date'].max().date()
rango_fechas_seleccionado = st.sidebar.date_input(
    "Selecciona Rango de Fechas:",
    (min_date, max_date)
)

# Convertir fechas seleccionadas a datetime
fecha_inicio_seleccionada = pd.to_datetime(rango_fechas_seleccionado[0])
fecha_fin_seleccionada = pd.to_datetime(rango_fechas_seleccionado[1])


# Filtrar los datos según las selecciones
ventas_filtradas = ventas[
    (ventas['Branch'].isin(sucursales_seleccionadas)) &
    (ventas['Gender'].isin(generos_seleccionados)) &
    (ventas['Payment'].isin(tipos_pago_seleccionados)) &
    (ventas['Product line'].isin(lineas_producto_seleccionadas)) &
    (ventas['Total'] >= rango_total_seleccionado[0]) &
    (ventas['Total'] <= rango_total_seleccionado[1]) &
    (ventas['Date'] >= fecha_inicio_seleccionada) &
    (ventas['Date'] <= fecha_fin_seleccionada)
]

# Mostrar un mensaje si no hay datos con los filtros seleccionados
if ventas_filtradas.empty:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")
    st.stop()

# --- Visualizaciones ---

# 1. Evolución de las Ventas Totales
st.subheader("Evolución de las Ventas Totales a lo largo del Tiempo")
ventas_por_dias_filtrado = ventas_filtradas.groupby('Date')['Total'].sum().reset_index()
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(data=ventas_por_dias_filtrado, x='Date', y='Total', ax=ax1)
ax1.set_title('Evolución de las Ventas Totales')
ax1.set_xlabel('Fecha')
ax1.set_ylabel('Ventas Totales')
plt.xticks(rotation=45)
st.pyplot(fig1)

# 2. Ingresos por Línea de Producto
st.subheader("Ingresos por Línea de Producto")
ingresos_por_linea_producto_filtrado = ventas_filtradas.groupby('Product line')['Total'].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(10, 8))
ax2.pie(ingresos_por_linea_producto_filtrado, labels=ingresos_por_linea_producto_filtrado.index, autopct='%1.1f%%', startangle=140)
ax2.set_title('Distribución de Ingresos por Línea de Producto')
ax2.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig2)


# 3. Métodos de Pago Preferidos
st.subheader("Distribución de Métodos de Pago Preferidos")
payment_counts_filtered = ventas_filtradas['Payment'].value_counts()
fig3, ax3 = plt.subplots(figsize=(10, 8))
ax3.pie(payment_counts_filtered, labels=payment_counts_filtered.index, autopct='%1.1f%%', startangle=140)
ax3.set_title('Distribución de Métodos de Pago Preferidos')
ax3.axis('equal')
st.pyplot(fig3)

# 4. Composición del Ingreso Bruto por Sucursal y Línea de Producto
st.subheader("Composición del Ingreso Bruto por Sucursal y Línea de Producto")
fig4, ax4 = plt.subplots(figsize=(14, 7))
sns.barplot(data=ventas_filtradas, x='Branch', y='gross income', hue='Product line', estimator=sum, ax=ax4)
ax4.set_title('Composición del Ingreso Bruto por Sucursal y Línea de Producto')
ax4.set_xlabel('Sucursal')
ax4.set_ylabel('Ingreso Bruto Total')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig4)


# Información adicional (opcional)
st.markdown("---")
st.markdown("Este dashboard interactivo te permite explorar las ventas de la tienda de conveniencia aplicando diferentes filtros.")
