import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Dashboard Montajes - Comparativo", layout="wide", page_icon="📊")

# ============================================================
# CARGA DE DATOS
# ============================================================
@st.cache_data
def cargar_datos(archivo, mes_nombre=""):
    if archivo is None:
        return None

    # Tabla5 vive en DATA!A6:Q236 → header en fila 6 (índice 5)
    df = pd.read_excel(archivo, sheet_name="DATA", header=5, usecols="A:Q")
    df.columns = [c.strip() for c in df.columns]

    # Normalizar texto (hay espacios sobrantes en MONTADOR, CLIENTE, etc.)
    for col in ["MONTADOR", "NOMBRE DEL MONTADOR  / LÍDER", "CLIENTE", "PRODUCTO"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Forzar numéricos (los #N/D se vuelven NaN)
    for col in ["TIEMPO BRUTO (MIN)", "TIEMPOS PAROS/MUERTOS",
                "TIEMPO NETO", "TIEMPO PROGRAMADO", "DÍA"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Marcar montaje / desmontaje (vienen como "X" o vacío)
    df["ES_MONTAJE"]    = df["MONTAJE (X)"].astype(str).str.strip().str.upper() == "X"
    df["ES_DESMONTAJE"] = df["DESMONTAJE (X)"].astype(str).str.strip().str.upper() == "X"
    df["TIPO"] = df.apply(
        lambda r: "Montaje" if r["ES_MONTAJE"] else ("Desmontaje" if r["ES_DESMONTAJE"] else "N/D"),
        axis=1,
    )

    # Filtrar filas válidas: requieren montador y tiempo neto numérico > 0
    df = df[df["MONTADOR"].notna() & (df["MONTADOR"] != "nan") & (df["MONTADOR"] != "")]
    df = df[df["TIEMPO NETO"].notna() & (df["TIEMPO NETO"] > 0)]

    # Convertir serial de fecha Excel → fecha real (origen 1899-12-30)
    df["FECHA"] = pd.to_datetime(df["DÍA"], origin="1899-12-30", unit="D", errors="coerce")

    if mes_nombre:
        df["MES_LABEL"] = mes_nombre

    return df.reset_index(drop=True)

# ============================================================
# SIDEBAR — CARGA DE ARCHIVOS Y FILTROS
# ============================================================
st.sidebar.title("⚙️ Configuración")
st.sidebar.markdown("### 📁 Carga de archivos")

archivo1 = st.sidebar.file_uploader("Archivo MES 1", type=["xlsx"], key="file1")
mes1_nombre = st.sidebar.text_input("Nombre mes 1", value="Marzo", key="mes1_name")

archivo2 = st.sidebar.file_uploader("Archivo MES 2 (Opcional)", type=["xlsx"], key="file2")
mes2_nombre = st.sidebar.text_input("Nombre mes 2", value="Abril", key="mes2_name")

if archivo1 is None:
    ruta_local = Path("MARZO.xlsx")
    if ruta_local.exists():
        archivo1 = ruta_local
        mes1_nombre = "Marzo"
    else:
        st.info("⬆️ Sube al menos un archivo Excel para comenzar.")
        st.stop()

# Cargar datos
df1 = cargar_datos(archivo1, mes1_nombre)
df2 = cargar_datos(archivo2, mes2_nombre) if archivo2 else None

# Si hay dos archivos, combinar para obtener lista completa de montadores
if df2 is not None:
    df_combined = pd.concat([df1, df2], ignore_index=True)
    todos_montadores = sorted(df_combined["MONTADOR"].unique())
else:
    todos_montadores = sorted(df1["MONTADOR"].unique())

# ============================================================
# FILTROS EN SIDEBAR
# ============================================================
st.sidebar.markdown("### 🔍 Filtros")

st.sidebar.markdown("**Selecciona montadores:**")
montadores_seleccionados = st.sidebar.multiselect(
    "Montadores",
    todos_montadores,
    default=todos_montadores,
    key="montador_filter"
)

clientes = sorted(df1["CLIENTE"].dropna().unique())
if df2 is not None:
    clientes = sorted(set(clientes) | set(df2["CLIENTE"].dropna().unique()))

clientes_seleccionados = st.sidebar.multiselect(
    "Clientes",
    clientes,
    default=clientes,
    key="cliente_filter"
)

tipos_seleccionados = st.sidebar.multiselect(
    "Tipo de operación",
    ["Montaje", "Desmontaje"],
    default=["Montaje", "Desmontaje"],
    key="tipo_filter"
)

# Aplicar filtros
def aplicar_filtros(df):
    return df[
        df["MONTADOR"].isin(montadores_seleccionados)
        & df["CLIENTE"].isin(clientes_seleccionados)
        & df["TIPO"].isin(tipos_seleccionados)
    ].copy()

dff1 = aplicar_filtros(df1)
dff2 = aplicar_filtros(df2) if df2 is not None else None

if dff1.empty:
    st.warning("No hay datos en MES 1 con los filtros seleccionados.")
    st.stop()

# ============================================================
# TÍTULO
# ============================================================
if df2 is not None:
    st.title("📊 Comparativo de Montajes")
    st.caption(f"{mes1_nombre} vs {mes2_nombre}")
else:
    st.title(f"📊 Dashboard de Montajes — {mes1_nombre}")
    st.caption("Análisis detallado de operaciones")

# ============================================================
# FUNCIÓN PARA CALCULAR KPIs
# ============================================================
def calcular_kpis(df):
    dff_ef = df.dropna(subset=["TIEMPO PROGRAMADO", "TIEMPO NETO"])
    dff_ef = dff_ef[dff_ef["TIEMPO NETO"] > 0]

    total_ops = len(df)
    total_montajes = int(df["ES_MONTAJE"].sum())
    total_desmontajes = int(df["ES_DESMONTAJE"].sum())
    horas_netas = df["TIEMPO NETO"].sum() / 60
    paros_min = df["TIEMPOS PAROS/MUERTOS"].fillna(0).sum()
    bruto_min = df["TIEMPO BRUTO (MIN)"].fillna(0).sum()
    pct_paros = (paros_min / bruto_min * 100) if bruto_min else 0
    eficiencia = (dff_ef["TIEMPO PROGRAMADO"].sum() / dff_ef["TIEMPO NETO"].sum() * 100) if len(dff_ef) else 0
    cumplimiento = (dff_ef["TIEMPO NETO"] <= dff_ef["TIEMPO PROGRAMADO"]).mean() * 100 if len(dff_ef) else 0

    return {
        "Operaciones": total_ops,
        "Montajes": total_montajes,
        "Desmontajes": total_desmontajes,
        "Horas netas": horas_netas,
        "Eficiencia (%)": eficiencia,
        "Cumplimiento (%)": cumplimiento,
        "% Paros": pct_paros
    }

kpis1 = calcular_kpis(dff1)
kpis2 = calcular_kpis(dff2) if dff2 is not None else None

# ============================================================
# KPIs COMPARATIVOS
# ============================================================
if df2 is not None and dff2 is not None and not dff2.empty:
    st.markdown("### 📊 KPIs Comparativos")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(f"{mes1_nombre} - Operaciones", f"{kpis1['Operaciones']:,}")
    with col2:
        st.metric(f"{mes2_nombre} - Operaciones", f"{kpis2['Operaciones']:,}" if kpis2 else "N/A")
    with col3:
        delta_ops = kpis2['Operaciones'] - kpis1['Operaciones'] if kpis2 else 0
        st.metric("Diferencia", f"{delta_ops:+,}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"{mes1_nombre} - Eficiencia", f"{kpis1['Eficiencia (%)']:.1f}%")
    with col2:
        st.metric(f"{mes2_nombre} - Eficiencia", f"{kpis2['Eficiencia (%)']:.1f}%" if kpis2 else "N/A")
    with col3:
        delta_ef = kpis2['Eficiencia (%)'] - kpis1['Eficiencia (%)'] if kpis2 else 0
        st.metric("Diferencia", f"{delta_ef:+.1f}%",
                 delta_color="normal" if delta_ef >= 0 else "inverse")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"{mes1_nombre} - Horas netas", f"{kpis1['Horas netas']:.1f} h")
    with col2:
        st.metric(f"{mes2_nombre} - Horas netas", f"{kpis2['Horas netas']:.1f} h" if kpis2 else "N/A")
    with col3:
        delta_hrs = kpis2['Horas netas'] - kpis1['Horas netas'] if kpis2 else 0
        st.metric("Diferencia", f"{delta_hrs:+.1f} h")

    st.divider()

else:
    # MES 1 SOLO
    st.markdown(f"### 📊 KPIs — {mes1_nombre}")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Operaciones", f"{kpis1['Operaciones']:,}")
    c2.metric("Montajes / Desmontajes", f"{kpis1['Montajes']} / {kpis1['Desmontajes']}")
    c3.metric("Horas netas", f"{kpis1['Horas netas']:.1f} h")
    c4.metric("Eficiencia", f"{kpis1['Eficiencia (%)']:.1f}%")
    c5.metric("Cumplimiento", f"{kpis1['Cumplimiento (%)']:.1f}%",
             delta=f"% paros: {kpis1['% Paros']:.1f}%", delta_color="off")

    st.divider()

# ============================================================
# COMPARACIÓN: EFICIENCIA POR MONTADOR
# ============================================================
st.subheader("👷 Eficiencia por montador")

def get_montador_stats(df):
    dff_ef = df.dropna(subset=["TIEMPO PROGRAMADO", "TIEMPO NETO"])
    dff_ef = dff_ef[dff_ef["TIEMPO NETO"] > 0]

    agg = (
        dff_ef.groupby(["MONTADOR", "NOMBRE DEL MONTADOR  / LÍDER"], dropna=False)
        .agg(
            Operaciones=("ID", "count"),
            Tiempo_neto_min=("TIEMPO NETO", "sum"),
            Tiempo_programado_min=("TIEMPO PROGRAMADO", "sum"),
        )
        .reset_index()
    )
    agg["Eficiencia (%)"] = agg["Tiempo_programado_min"] / agg["Tiempo_neto_min"] * 100
    return agg.sort_values("Eficiencia (%)", ascending=False)

agg1 = get_montador_stats(dff1)

if df2 is not None and dff2 is not None and not dff2.empty:
    agg2 = get_montador_stats(dff2)

    # Gráfico comparativo
    agg_merge = agg1[["MONTADOR", "Eficiencia (%)"]].copy()
    agg_merge.columns = ["MONTADOR", mes1_nombre]
    agg2_temp = agg2[["MONTADOR", "Eficiencia (%)"]].copy()
    agg2_temp.columns = ["MONTADOR", mes2_nombre]

    agg_compare = agg_merge.merge(agg2_temp, on="MONTADOR", how="outer").fillna(0)
    agg_compare = agg_compare.sort_values(mes1_nombre, ascending=False)

    fig = px.bar(
        agg_compare.melt(id_vars="MONTADOR", var_name="Mes", value_name="Eficiencia (%)"),
        x="MONTADOR", y="Eficiencia (%)", color="Mes", barmode="group",
        title=f"Eficiencia comparativa por montador — {mes1_nombre} vs {mes2_nombre}",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"]
    )
    fig.add_hline(y=100, line_dash="dash", line_color="gray")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**{mes1_nombre}**")
        st.dataframe(agg1[["MONTADOR", "Operaciones", "Eficiencia (%)"]].round(1),
                    hide_index=True, use_container_width=True)
    with col2:
        st.write(f"**{mes2_nombre}**")
        st.dataframe(agg2[["MONTADOR", "Operaciones", "Eficiencia (%)"]].round(1),
                    hide_index=True, use_container_width=True)

else:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        fig = px.bar(
            agg1, x="MONTADOR", y="Eficiencia (%)",
            color="Eficiencia (%)", color_continuous_scale="RdYlGn",
            title="Eficiencia por montador"
        )
        fig.add_hline(y=100, line_dash="dash", line_color="gray")
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.dataframe(agg1[["MONTADOR", "Operaciones", "Eficiencia (%)"]].round(1),
                    hide_index=True, use_container_width=True)

st.divider()

# ============================================================
# ANÁLISIS POR CLIENTE
# ============================================================
st.subheader("🏢 Análisis por cliente")

def get_cliente_stats(df):
    dff_ef = df.dropna(subset=["TIEMPO PROGRAMADO", "TIEMPO NETO"])
    dff_ef = dff_ef[dff_ef["TIEMPO NETO"] > 0]

    agg = (
        dff_ef.groupby("CLIENTE", dropna=False)
        .agg(
            Operaciones=("ID", "count"),
            Tiempo_neto_min=("TIEMPO NETO", "sum"),
            Tiempo_programado_min=("TIEMPO PROGRAMADO", "sum"),
        )
        .reset_index()
    )
    agg["Horas netas"] = agg["Tiempo_neto_min"] / 60
    agg["Eficiencia (%)"] = agg["Tiempo_programado_min"] / agg["Tiempo_neto_min"] * 100
    return agg.sort_values("Operaciones", ascending=False)

agg_cli1 = get_cliente_stats(dff1)

if df2 is not None and dff2 is not None and not dff2.empty:
    agg_cli2 = get_cliente_stats(dff2)

    col_c, col_d = st.columns(2)
    with col_c:
        fig = px.bar(agg_cli1, x="CLIENTE", y="Operaciones",
                    title=f"Operaciones por cliente — {mes1_nombre}")
        st.plotly_chart(fig, use_container_width=True)
    with col_d:
        fig = px.bar(agg_cli2, x="CLIENTE", y="Operaciones",
                    title=f"Operaciones por cliente — {mes2_nombre}")
        st.plotly_chart(fig, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.write(f"**{mes1_nombre}**")
        st.dataframe(agg_cli1.round(1), hide_index=True, use_container_width=True)
    with col_d:
        st.write(f"**{mes2_nombre}**")
        st.dataframe(agg_cli2.round(1), hide_index=True, use_container_width=True)

else:
    col_c, col_d = st.columns(2)
    with col_c:
        fig = px.bar(agg_cli1, x="CLIENTE", y="Operaciones",
                    title="Volumen de operaciones por cliente")
        st.plotly_chart(fig, use_container_width=True)
    with col_d:
        fig = px.pie(agg_cli1, names="CLIENTE", values="Horas netas",
                    title="Distribución de horas netas", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(agg_cli1.round(1), hide_index=True, use_container_width=True)

st.divider()

# ============================================================
# MONTAJES vs DESMONTAJES POR PRODUCTO
# ============================================================
st.subheader("🔧 Montajes y desmontajes por producto")

def get_producto_stats(df):
    agg = (
        df.groupby("PRODUCTO")
        .agg(
            Montajes=("ES_MONTAJE", "sum"),
            Desmontajes=("ES_DESMONTAJE", "sum"),
        )
        .reset_index()
    )
    agg["Total"] = agg["Montajes"] + agg["Desmontajes"]
    return agg.sort_values("Total", ascending=False)

agg_prod1 = get_producto_stats(dff1)

if df2 is not None and dff2 is not None and not dff2.empty:
    agg_prod2 = get_producto_stats(dff2)

    top_n = st.slider("Top N productos", 5, 30, 15)
    top_prod1 = agg_prod1.head(top_n)
    top_prod2 = agg_prod2.head(top_n)

    col_e, col_f = st.columns(2)
    with col_e:
        fig = px.bar(
            top_prod1.melt(id_vars="PRODUCTO", value_vars=["Montajes", "Desmontajes"],
                          var_name="Tipo", value_name="Cantidad"),
            x="PRODUCTO", y="Cantidad", color="Tipo", barmode="group",
            title=f"Top {top_n} productos — {mes1_nombre}"
        )
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col_f:
        fig = px.bar(
            top_prod2.melt(id_vars="PRODUCTO", value_vars=["Montajes", "Desmontajes"],
                          var_name="Tipo", value_name="Cantidad"),
            x="PRODUCTO", y="Cantidad", color="Tipo", barmode="group",
            title=f"Top {top_n} productos — {mes2_nombre}"
        )
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

else:
    top_n = st.slider("Top N productos", 5, 30, 15)
    top_prod1 = agg_prod1.head(top_n)

    fig = px.bar(
        top_prod1.melt(id_vars="PRODUCTO", value_vars=["Montajes", "Desmontajes"],
                      var_name="Tipo", value_name="Cantidad"),
        x="PRODUCTO", y="Cantidad", color="Tipo", barmode="group",
        title=f"Top {top_n} productos"
    )
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ============================================================
# DETALLE Y DESCARGA
# ============================================================
st.subheader("📋 Detalle y descarga")

tab1, tab2 = st.tabs([f"{mes1_nombre}", f"{mes2_nombre}"] if df2 is not None else [f"{mes1_nombre}", "Comparación"])

with tab1:
    st.write(f"**{mes1_nombre}** - Operaciones filtradas")
    st.dataframe(
        dff1[["FECHA", "MONTADOR", "NOMBRE DEL MONTADOR  / LÍDER", "PRODUCTO",
              "CLIENTE", "TIPO", "TIEMPO NETO", "TIEMPO PROGRAMADO",
              "TIEMPOS PAROS/MUERTOS"]],
        hide_index=True, use_container_width=True,
    )
    st.download_button("⬇️ Descargar CSV", dff1.to_csv(index=False).encode("utf-8"),
                      f"operaciones_{mes1_nombre}.csv", "text/csv")

with tab2:
    if df2 is not None and dff2 is not None and not dff2.empty:
        st.write(f"**{mes2_nombre}** - Operaciones filtradas")
        st.dataframe(
            dff2[["FECHA", "MONTADOR", "NOMBRE DEL MONTADOR  / LÍDER", "PRODUCTO",
                  "CLIENTE", "TIPO", "TIEMPO NETO", "TIEMPO PROGRAMADO",
                  "TIEMPOS PAROS/MUERTOS"]],
            hide_index=True, use_container_width=True,
        )
        st.download_button("⬇️ Descargar CSV", dff2.to_csv(index=False).encode("utf-8"),
                          f"operaciones_{mes2_nombre}.csv", "text/csv")
    else:
        st.info("Carga un segundo archivo para ver la comparación detallada.")
