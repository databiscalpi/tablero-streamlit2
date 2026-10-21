import streamlit as st
import pandas as pd
import plotly.express as px
from models.facturacion_maquila import get_factura_maquila

# ================= TÍTULO Y CARGA DE DATOS =================
st.title("Facturación Maquila 2026")

# Cargar datos usando tu modelo
df_factura_maquila = get_factura_maquila()

# Validar que haya datos
if df_factura_maquila.empty:
    st.warning("⚠️ No hay datos disponibles para mostrar.")
    st.stop()

# Asegurar que la fecha sea tipo datetime (por si el modelo la devuelve como string)
df_factura_maquila['DocDate'] = pd.to_datetime(df_factura_maquila['DocDate'])

# Mostrar la tabla cruda primero (como tenías originalmente)
st.subheader("📋 Datos Crudos")
st.dataframe(df_factura_maquila, use_container_width=True)

st.divider()

# ================= DASHBOARD Y GRÁFICAS =================
st.header("📈 Evolución de Ingresos por Cliente")

# --- Filtros en el Sidebar ---
st.sidebar.subheader(" Filtros del Dashboard")

# Rango de fechas
min_fecha = df_factura_maquila['DocDate'].min().date()
max_fecha = df_factura_maquila['DocDate'].max().date()

fecha_inicio, fecha_fin = st.sidebar.date_input(
    "Rango de fechas",
    value=(min_fecha, max_fecha),
    min_value=min_fecha,
    max_value=max_fecha
)

# Selector de cliente(s)
clientes = sorted(df_factura_maquila['Cliente'].unique().tolist())
clientes_sel = st.sidebar.multiselect(
    "Clientes",
    options=clientes,
    default=clientes # O puedes poner default=clientes[:5] para no saturar
)

# Granularidad y Tipo de gráfico
granularidad = st.sidebar.radio("📅 Ver por:", ["📆 Mes", "📅 Día"], horizontal=True)
tipo_grafico = st.sidebar.radio("📊 Tipo de gráfico:", ["Líneas", "Barras", "Área"], horizontal=True)

# --- Aplicar Filtros ---
df_filtrado = df_factura_maquila[
    (df_factura_maquila['DocDate'].dt.date >= fecha_inicio) &
    (df_factura_maquila['DocDate'].dt.date <= fecha_fin) &
    (df_factura_maquila['Cliente'].isin(clientes_sel))
].copy()

if df_filtrado.empty:
    st.warning("️ No hay datos para los filtros seleccionados.")
    st.stop()

# --- Agregar por Periodo ---
if granularidad == "📆 Mes":
    df_filtrado['Periodo'] = df_filtrado['DocDate'].dt.to_period('M').astype(str)
else:
    df_filtrado['Periodo'] = df_filtrado['DocDate'].dt.strftime('%Y-%m-%d')

df_agg = df_filtrado.groupby(['Periodo', 'Cliente'])['Valor_ingresado'].sum().reset_index()

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Ingresado", f"${df_filtrado['Valor_ingresado'].sum():,.0f}")
col2.metric("📦 Transacciones", f"{len(df_filtrado):,}")
col3.metric("👥 Clientes", f"{df_filtrado['Cliente'].nunique()}")
col4.metric("📈 Promedio", f"${df_filtrado['Valor_ingresado'].mean():,.0f}")

st.divider()

# --- Gráfica Principal ---
st.subheader(f"Evolución de Ingresos ({granularidad})")

if tipo_grafico == "Líneas":
    fig = px.line(df_agg, x='Periodo', y='Valor_ingresado', color='Cliente', markers=True)
elif tipo_grafico == "Barras":
    # Si hay muchos clientes, apila las barras; si no, las agrupa
    barmode = 'stack' if len(clientes_sel) > 5 else 'group'
    fig = px.bar(df_agg, x='Periodo', y='Valor_ingresado', color='Cliente', barmode=barmode)
else:  # Área
    fig = px.area(df_agg, x='Periodo', y='Valor_ingresado', color='Cliente')

fig.update_layout(
    height=500,
    hovermode='x unified',
    xaxis_title=granularidad.split(" ")[1],
    yaxis_title='Valor Ingresado',
    template='plotly_white'
)
fig.update_yaxes(tickformat=",.0f")
st.plotly_chart(fig, use_container_width=True)

# --- Tabla Dinámica y Descarga ---
with st.expander("📋 Ver datos agrupados y descargar"):
    tabla_pivote = df_agg.pivot(index='Periodo', columns='Cliente', values='Valor_ingresado').fillna(0).astype(int)
    st.dataframe(tabla_pivote, use_container_width=True)
    
    csv = df_agg.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name=f"evolucion_maquila_{granularidad.split(' ')[1]}.csv",
        mime="text/csv"
    )

# --- Top 10 Clientes ---
st.subheader("🏆 Top 10 Clientes del Periodo")
top_clientes = df_filtrado.groupby('Cliente')['Valor_ingresado'].sum().sort_values(ascending=False).head(10)

fig_top = px.bar(
    x=top_clientes.values,
    y=top_clientes.index,
    orientation='h',
    labels={'x': 'Total Ingresado', 'y': 'Cliente'},
    color=top_clientes.values,
    color_continuous_scale='Blues'
)
fig_top.update_layout(showlegend=False, height=400, template='plotly_white')
fig_top.update_xaxes(tickformat=",.0f")
st.plotly_chart(fig_top, use_container_width=True)