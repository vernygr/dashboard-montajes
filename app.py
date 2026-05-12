import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Montajes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS
st.markdown("""
    <style>
        .kpi-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #3b82f6;
            margin-bottom: 10px;
        }
        .kpi-value {
            font-size: 32px;
            font-weight: bold;
            color: #111827;
        }
        .kpi-label {
            font-size: 14px;
            color: #6b7280;
            margin-top: 5px;
        }
        .status-excellent { color: #10b981; font-weight: bold; }
        .status-acceptable { color: #f59e0b; font-weight: bold; }
        .status-poor { color: #ef4444; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📁 Cargar Datos")
st.sidebar.markdown("---")

# Instrucciones
with st.sidebar.expander("ℹ️ Instrucciones", expanded=False):
    st.markdown("""
    ### Pasos para actualizar el dashboard:
    1. Descarga tu archivo Excel `MARZO.xlsx` (o el mes actual)
    2. Asegúrate que tenga la hoja **"DATA"**
    3. Carga el archivo usando el botón de abajo
    4. El dashboard se actualizará automáticamente

    **Estructura esperada:**
    - La hoja "DATA" debe tener las columnas:
      - MES, DÍA, MONTADOR, NOMBRE DEL MONTADOR / LÍDER, PRODUCTO, CLIENTE, INY
      - MONTAJE (X), DESMONTAJE (X), ID
      - HORA DE INICIO, HORA DE FINALIZACIÓN
      - TIEMPO TOTAL (HORAS), TIEMPO BRUTO (MIN)
      - TIEMPOS PAROS/MUERTOS, TIEMPO NETO, TIEMPO PROGRAMADO
    """)

# Cargar archivo Excel
uploaded_file = st.sidebar.file_uploader(
    "Cargar archivo Excel",
    type=['xlsx', 'xls'],
    help="Selecciona tu archivo Excel con los datos de montajes"
)

def load_and_process_data(file):
    """Carga y procesa los datos del Excel"""
    try:
        # Leer Excel desde fila 6 (donde empieza el encabezado real)
        df = pd.read_excel(file, sheet_name='DATA', header=5)

        # Limpiar nombres de columnas - remover espacios extras
        df.columns = df.columns.str.strip()

        # Limpiar datos
        df = df.dropna(subset=['TIEMPO NETO', 'TIEMPO PROGRAMADO'], how='all')

        # Convertir a numérico
        df['TIEMPO NETO'] = pd.to_numeric(df['TIEMPO NETO'], errors='coerce')
        df['TIEMPO PROGRAMADO'] = pd.to_numeric(df['TIEMPO PROGRAMADO'], errors='coerce')

        if 'TIEMPO BRUTO (MIN)' in df.columns:
            df['TIEMPO BRUTO (MIN)'] = pd.to_numeric(df['TIEMPO BRUTO (MIN)'], errors='coerce')

        # Filtrar registros válidos
        df = df[df['TIEMPO PROGRAMADO'] > 0].copy()
        df = df.dropna(subset=['TIEMPO NETO', 'TIEMPO PROGRAMADO'])

        return df
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
        st.error(f"Verifica que la hoja se llama 'DATA' y los datos comienzan en la fila 6")
        return None

def calculate_kpis(df):
    """Calcula los KPIs principales"""
    total_ops = len(df)
    horas_netas = df['TIEMPO NETO'].sum()
    horas_programadas = df['TIEMPO PROGRAMADO'].sum()
    eficiencia = (horas_netas / horas_programadas * 100) if horas_programadas > 0 else 0

    return {
        'eficiencia': eficiencia,
        'total_operaciones': total_ops,
        'horas_productivas': horas_netas,
        'montadores_activos': df['MONTADOR'].nunique() if 'MONTADOR' in df.columns else 0
    }

def get_montador_stats(df):
    """Obtiene estadísticas por montador"""
    if 'MONTADOR' not in df.columns:
        return pd.DataFrame()

    stats = df.groupby('MONTADOR').agg({
        'TIEMPO NETO': 'sum',
        'TIEMPO PROGRAMADO': 'sum'
    }).reset_index()

    stats['OPERACIONES'] = df.groupby('MONTADOR').size().values
    stats['EFICIENCIA %'] = (stats['TIEMPO NETO'] / stats['TIEMPO PROGRAMADO'] * 100).round(2)
    stats = stats.sort_values('EFICIENCIA %', ascending=False)

    return stats

def get_cliente_stats(df):
    """Obtiene estadísticas por cliente"""
    if 'CLIENTE' not in df.columns:
        return pd.DataFrame()

    df_clean = df.dropna(subset=['CLIENTE'])

    stats = df_clean.groupby('CLIENTE').agg({
        'TIEMPO NETO': 'sum',
        'TIEMPO PROGRAMADO': 'sum'
    }).reset_index()

    stats['OPERACIONES'] = df_clean.groupby('CLIENTE').size().values
    stats['EFICIENCIA %'] = (stats['TIEMPO NETO'] / stats['TIEMPO PROGRAMADO'] * 100).round(2)
    stats = stats.sort_values('OPERACIONES', ascending=False)

    return stats

def get_producto_stats(df):
    """Obtiene estadísticas por producto"""
    if 'PRODUCTO' not in df.columns:
        return pd.DataFrame()

    df_clean = df.dropna(subset=['PRODUCTO'])

    stats = df_clean['PRODUCTO'].value_counts().reset_index()
    stats.columns = ['PRODUCTO', 'OPERACIONES']

    return stats

# Contenido principal
st.title("📊 Dashboard Montajes")
st.markdown("Análisis de KPIs de producción - Actualización Semanal")
st.markdown("---")

if uploaded_file is not None:
    # Cargar y procesar datos
    df = load_and_process_data(uploaded_file)

    if df is not None and len(df) > 0:
        # Mostrar información del archivo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📅 Registros cargados", len(df))
        with col2:
            mes = df['MES'].iloc[0] if 'MES' in df.columns else "N/A"
            st.metric("📆 Mes", mes)
        with col3:
            st.metric("⏱️ Última actualización", datetime.now().strftime("%d/%m/%Y %H:%M"))

        st.markdown("---")

        # Calcular KPIs
        kpis = calculate_kpis(df)

        # Mostrar KPIs principales
        st.subheader("📈 KPIs Principales")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div class="kpi-container">
                    <div class="kpi-label">Eficiencia Operativa</div>
                    <div class="kpi-value">{kpis['eficiencia']:.1f}%</div>
                    <div class="kpi-label">Tiempo neto vs programado</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="kpi-container">
                    <div class="kpi-label">Total Operaciones</div>
                    <div class="kpi-value">{kpis['total_operaciones']}</div>
                    <div class="kpi-label">Operaciones completadas</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            horas_k = kpis['horas_productivas'] / 1000
            st.markdown(f"""
                <div class="kpi-container">
                    <div class="kpi-label">Horas Productivas</div>
                    <div class="kpi-value">{horas_k:.1f}K</div>
                    <div class="kpi-label">Horas netas totales</div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div class="kpi-container">
                    <div class="kpi-label">Montadores Activos</div>
                    <div class="kpi-value">{kpis['montadores_activos']}</div>
                    <div class="kpi-label">Equipo operativo</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Tabs para diferentes vistas
        tab1, tab2, tab3 = st.tabs(["📊 Eficiencia Operativa", "🎯 Productividad", "📈 Tendencias"])

        # TAB 1: Eficiencia Operativa
        with tab1:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Eficiencia por Montador")
                montador_stats = get_montador_stats(df)

                if len(montador_stats) > 0:
                    fig = px.bar(
                        montador_stats,
                        x='EFICIENCIA %',
                        y='MONTADOR',
                        orientation='h',
                        color='EFICIENCIA %',
                        color_continuous_scale='RdYlGn',
                        range_color=[0, 100],
                        title="",
                        labels={'EFICIENCIA %': 'Eficiencia (%)', 'MONTADOR': 'Montador'}
                    )
                    fig.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("Eficiencia por Cliente")
                cliente_stats = get_cliente_stats(df)

                if len(cliente_stats) > 0:
                    fig = px.line(
                        cliente_stats.head(5),
                        x='CLIENTE',
                        y='EFICIENCIA %',
                        markers=True,
                        title="",
                        labels={'EFICIENCIA %': 'Eficiencia (%)', 'CLIENTE': 'Cliente'},
                        range_y=[0, 100]
                    )
                    fig.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)

        # TAB 2: Productividad
        with tab2:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Operaciones por Montador")
                montador_stats = get_montador_stats(df)

                if len(montador_stats) > 0:
                    fig = px.bar(
                        montador_stats,
                        x='MONTADOR',
                        y='OPERACIONES',
                        color='OPERACIONES',
                        color_continuous_scale='Blues',
                        title=""
                    )
                    fig.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("Distribución por Producto")
                producto_stats = get_producto_stats(df)

                if len(producto_stats) > 0:
                    fig = px.pie(
                        producto_stats.head(5),
                        values='OPERACIONES',
                        names='PRODUCTO',
                        title=""
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)

        # TAB 3: Tendencias
        with tab3:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Clientes Top (por Volumen)")
                cliente_stats = get_cliente_stats(df)

                if len(cliente_stats) > 0:
                    fig = px.bar(
                        cliente_stats.head(5),
                        x='CLIENTE',
                        y='OPERACIONES',
                        color='OPERACIONES',
                        color_continuous_scale='Viridis',
                        title=""
                    )
                    fig.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("Productos Top (por Volumen)")
                producto_stats = get_producto_stats(df)

                if len(producto_stats) > 0:
                    fig = px.bar(
                        producto_stats.head(5),
                        x='PRODUCTO',
                        y='OPERACIONES',
                        color='OPERACIONES',
                        color_continuous_scale='Oranges',
                        title=""
                    )
                    fig.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Tabla detallada de montadores
        st.subheader("👥 Resumen Detallado de Montadores")
        montador_stats = get_montador_stats(df)

        if len(montador_stats) > 0:
            # Formatear para mostrar
            display_df = montador_stats.copy()
            display_df['EFICIENCIA %'] = display_df['EFICIENCIA %'].apply(lambda x: f"{x:.1f}%")
            display_df['ESTADO'] = montador_stats['EFICIENCIA %'].apply(
                lambda x: "✅ Excelente" if x >= 70 else "⚠️ Aceptable" if x >= 50 else "❌ Necesita mejora"
            )
            display_df['TIEMPO NETO'] = display_df['TIEMPO NETO'].round(2)
            display_df['TIEMPO PROGRAMADO'] = display_df['TIEMPO PROGRAMADO'].round(2)

            st.dataframe(
                display_df[['MONTADOR', 'OPERACIONES', 'EFICIENCIA %', 'ESTADO']],
                use_container_width=True,
                hide_index=True
            )

        # Tabla de clientes
        st.subheader("🏢 Resumen por Cliente")
        cliente_stats = get_cliente_stats(df)

        if len(cliente_stats) > 0:
            display_cliente = cliente_stats.copy()
            display_cliente['EFICIENCIA %'] = display_cliente['EFICIENCIA %'].apply(lambda x: f"{x:.1f}%")

            st.dataframe(
                display_cliente[['CLIENTE', 'OPERACIONES', 'EFICIENCIA %']],
                use_container_width=True,
                hide_index=True
            )

        # Exportar datos
        st.markdown("---")
        st.subheader("📥 Descargar Datos")

        col1, col2 = st.columns(2)

        with col1:
            # Exportar KPIs a CSV
            kpi_export = pd.DataFrame([
                {
                    'Métrica': 'Eficiencia Operativa (%)',
                    'Valor': f"{kpis['eficiencia']:.2f}",
                    'Fecha': datetime.now().strftime("%d/%m/%Y")
                },
                {
                    'Métrica': 'Total Operaciones',
                    'Valor': kpis['total_operaciones'],
                    'Fecha': datetime.now().strftime("%d/%m/%Y")
                },
                {
                    'Métrica': 'Horas Productivas',
                    'Valor': f"{kpis['horas_productivas']:.0f}",
                    'Fecha': datetime.now().strftime("%d/%m/%Y")
                }
            ])

            csv = kpi_export.to_csv(index=False)
            st.download_button(
                label="📊 Descargar KPIs (CSV)",
                data=csv,
                file_name=f"kpis_montajes_{datetime.now().strftime('%d_%m_%Y')}.csv",
                mime="text/csv"
            )

        with col2:
            # Exportar datos procesados
            csv = df.to_csv(index=False)
            st.download_button(
                label="📋 Descargar Datos Procesados (CSV)",
                data=csv,
                file_name=f"datos_montajes_{datetime.now().strftime('%d_%m_%Y')}.csv",
                mime="text/csv"
            )

    else:
        st.warning("No se encontraron datos válidos en el archivo. Verifica que la hoja se llama 'DATA'.")

else:
    st.info("👈 Carga un archivo Excel para comenzar. El archivo debe tener la hoja 'DATA' con los datos de montajes.")

    # Mostrar información de ejemplo
    st.markdown("""
    ### 📋 Ejemplo de estructura esperada:

    | MES | DÍA | MONTADOR | NOMBRE DEL MONTADOR | PRODUCTO | CLIENTE | HORA DE INICIO | HORA DE FINALIZACIÓN | TIEMPO NETO | TIEMPO PROGRAMADO |
    |-----|-----|----------|---------------------|----------|---------|----------------|----------------------|-------------|-------------------|
    | MARZO | 2026-03-01 | AAJ | ALONSO | 90503564 | Arthro Care | 04:12:00 | 04:48:00 | 36.0 | 60 |
    | MARZO | 2026-03-01 | SAE | JOHNNY | 55855-001-R1 | Moog Medical | 22:38:00 | 23:04:00 | 26.0 | 107.5 |
    """)
