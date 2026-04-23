import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go

# Cargar datos desde SQLite
def get_datos():
    conn = sqlite3.connect('aemet_coruña.db')
    df = pd.read_sql_query('''
        SELECT fecha, tmax 
        FROM temperaturas 
        ORDER BY fecha
    ''', conn)
    conn.close()
    df['fecha'] = pd.to_datetime(df['fecha']).dt.date
    return df

df = get_datos()

# --- Layout de la app ---
# --- Layout de la app ---
st.title("Temperaturas máximas del mes — A CORUÑA")
st.caption("Estación 1387 · Datos diarios")

# Métricas resumen
col1, col2, col3 = st.columns(3)
col1.metric("Máxima del mes", f"{df['tmax'].max()} °C")
col2.metric("Mínima del mes", f"{df['tmax'].min()} °C")
col3.metric("Promedio mensual", f"{df['tmax'].mean():.1f} °C")

# --- Gráfica combinada ---
fig = go.Figure()

# Barras azules
fig.add_trace(go.Bar(
    x=df['fecha'],
    y=df['tmax'],
    name='Temp. máxima (barras)',
    marker_color='steelblue',
    opacity=0.7
))

# Línea roja
fig.add_trace(go.Scatter(
    x=df['fecha'],
    y=df['tmax'],
    name='Temp. máxima (línea)',
    mode='lines+markers',
    line=dict(color='red', width=2.5),
    marker=dict(color='red', size=6)
))

# Estilo del gráfico    
fig.update_layout(
    title='Evolución de temperatura máxima diaria',
    xaxis_title='Fecha',
    yaxis_title='Temperatura (°C)',
    legend=dict(orientation='h', y=-0.2),
    hovermode='x unified',
    plot_bgcolor='white',
    yaxis=dict(gridcolor='lightgrey')
)

st.plotly_chart(fig, use_container_width=True)

# Tabla de datos
with st.expander("Ver datos completos"):
    st.dataframe(df[['fecha', 'tmax']].rename(columns={
        'fecha': 'Fecha',
        'tmax': 'Temp. máxima (°C)'
    }), use_container_width=True)