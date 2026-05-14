import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Dashboard Montajes - Marzo", layout="wide", page_icon="📊")

# ============================================================
# CARGA DE DATOS
# ============================================================
@st.cache_data
def cargar_datos(archivo):
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

    return df.reset_index(drop=True)

# ============================================================
# SIDEBAR — CARGA Y FILTROS
# ============================================================
st.sidebar.title("⚙️ Configuración")
archivo = st.sidebar.file_uploader("Sube MARZO.xlsx", type=["xlsx"])

if archivo is None:
    ruta_local = Path("MARZO.xlsx")
    if ruta_local.exists():
        archivo = ruta_local
    else:
        st.info("⬆️ Sube el archivo MARZO.xlsx en la barra lateral para empezar.")
        st.stop()

df = cargar_datos(archivo)

st.sidebar.markdown("### 🔍 Filtros")
montadores = st.sidebar.multiselect("Montador", sorted(df["MONTADOR"].unique()),
                                     default=sorted(df["MONTADOR"].unique()))
clientes = st.sidebar.multiselect("Cliente", sorted(df["CLIENTE"].dropna().unique()),
                                   default=sorted(df["CLIENTE"].dropna().unique()))
tipos = st.sidebar.multiselect("Tipo de operación", ["Montaje", "Desmontaje"],
                                default=["Montaje", "Desmontaje"])

dff = df[
    df["MONTADOR"].isin(montadores)
    & df["CLIENTE"].isin(clientes)
    & df["TIPO"].isin(tipos)
].copy()

if dff.empty:
    st.warning("No hay datos con los filtros seleccionados.")
    st.stop()

# ============================================================
# KPIs PRINCIPALES
# ============================================================
# Fórmulas:
#   Eficiencia (%) = TIEMPO PROGRAMADO / TIEMPO NETO  (>100% = más rápido que estándar)
#   % Paros        = TIEMPOS PAROS/MUERTOS / TIEMPO BRUTO
#   Cumplimiento   = % de operaciones donde TIEMPO NETO <= TIEMPO PROGRAMADO
# ------------------------------------------------------------
dff_ef = dff.dropna(subset=["TIEMPO PROGRAMADO", "TIEMPO NETO"])
dff_ef = dff_ef[dff_ef["TIEMPO NETO"] > 0]

total_ops          = len(dff)
total_montajes     = int(dff["ES_MONTAJE"].sum())
total_desmontajes  = int(dff["ES_DESMONTAJE"].sum())
horas_netas        = dff["TIEMPO NETO"].sum() / 60
paros_min          = dff["TIEMPOS PAROS/MUERTOS"].fillna(0).sum()
bruto_min          = dff["TIEMPO BRUTO (MIN)"].fillna(0).sum()
pct_paros          = (paros_min / bruto_min * 100) if bruto_min else 0
eficiencia_global  = (dff_ef["TIEMPO PROGRAMADO"].sum() / dff_ef["TIEMPO NETO"].sum() * 100) if len(dff_ef) else 0
cumplimiento       = (dff_ef["TIEMPO NETO"] <= dff_ef["TIEMPO PROGRAMADO"]).mean() * 100 if len(dff_ef) else 0

st.title("📊 Dashboard de Montajes — Marzo")
st.caption("Eficiencia = Tiempo Programado / Tiempo Neto · Cumplimiento = % ops dentro del estándar")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Operaciones totales", f"{total_ops:,}")
c2.metric("Montajes / Desmontajes", f"{total_montajes} / {total_desmontajes}")
c3.metric("Horas netas trabajadas", f"{horas_netas:,.1f} h")
c4.metric("Eficiencia global", f"{eficiencia_global:,.1f}%",
          help=">100% = más rápido que el estándar")
c5.metric("Cumplimiento estándar", f"{cumplimiento:,.1f}%",
          delta=f"% paros: {pct_paros:,.1f}%", delta_color="off")

st.divider()

# ============================================================
# PRODUCTIVIDAD POR MONTADOR
# ============================================================
st.subheader("👷 Productividad por montador")

agg_mont = (
    dff_ef.groupby(["MONTADOR", "NOMBRE DEL MONTADOR  / LÍDER"], dropna=False)
    .agg(
        Operaciones=("ID", "count"),
        Tiempo_neto_min=("TIEMPO NETO", "sum"),
        Tiempo_programado_min=("TIEMPO PROGRAMADO", "sum"),
        Paros_min=("TIEMPOS PAROS/MUERTOS", "sum"),
    )
    .reset_index()
)
agg_mont["Horas netas"]    = agg_mont["Tiempo_neto_min"] / 60
agg_mont["Eficiencia (%)"] = agg_mont["Tiempo_programado_min"] / agg_mont["Tiempo_neto_min"] * 100
agg_mont = agg_mont.sort_values("Eficiencia (%)", ascending=False)

col_a, col_b = st.columns([2, 1])
with col_a:
    fig = px.bar(
        agg_mont, x="MONTADOR", y="Eficiencia (%)",
        color="Eficiencia (%)", color_continuous_scale="RdYlGn",
        hover_data=["NOMBRE DEL MONTADOR  / LÍDER", "Operaciones", "Horas netas"],
        title="Eficiencia por montador (% sobre tiempo estándar)",
    )
    fig.add_hline(y=100, line_dash="dash", line_color="gray",
                  annotation_text="Estándar 100%")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.dataframe(
        agg_mont[["MONTADOR", "NOMBRE DEL MONTADOR  / LÍDER",
                  "Operaciones", "Horas netas", "Eficiencia (%)"]]
        .round(1),
        hide_index=True, use_container_width=True,
    )

st.divider()

# ============================================================
# ANÁLISIS POR CLIENTE
# ============================================================
st.subheader("🏢 Análisis por cliente")

agg_cli = (
    dff_ef.groupby("CLIENTE", dropna=False)
    .agg(
        Operaciones=("ID", "count"),
        Tiempo_neto_min=("TIEMPO NETO", "sum"),
        Tiempo_programado_min=("TIEMPO PROGRAMADO", "sum"),
    )
    .reset_index()
)
agg_cli["Horas netas"]    = agg_cli["Tiempo_neto_min"] / 60
agg_cli["Eficiencia (%)"] = agg_cli["Tiempo_programado_min"] / agg_cli["Tiempo_neto_min"] * 100
agg_cli = agg_cli.sort_values("Operaciones", ascending=False)

col_c, col_d = st.columns(2)
with col_c:
    fig = px.bar(agg_cli, x="CLIENTE", y="Operaciones", color="Eficiencia (%)",
                 color_continuous_scale="RdYlGn",
                 title="Volumen de operaciones por cliente")
    st.plotly_chart(fig, use_container_width=True)
with col_d:
    fig = px.pie(agg_cli, names="CLIENTE", values="Horas netas",
                 title="Distribución de horas netas por cliente", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

st.dataframe(agg_cli.round(1), hide_index=True, use_container_width=True)

st.divider()

# ============================================================
# MONTAJES vs DESMONTAJES POR PRODUCTO
# ============================================================
st.subheader("🔧 Montajes y desmontajes por producto")

agg_prod = (
    dff.groupby("PRODUCTO")
    .agg(
        Montajes=("ES_MONTAJE", "sum"),
        Desmontajes=("ES_DESMONTAJE", "sum"),
        Tiempo_neto_min=("TIEMPO NETO", "sum"),
    )
    .reset_index()
)
agg_prod["Total"] = agg_prod["Montajes"] + agg_prod["Desmontajes"]
agg_prod = agg_prod.sort_values("Total", ascending=False)

top_n = st.slider("Top N productos por volumen", 5, 30, 15)
top_prod = agg_prod.head(top_n)

fig = px.bar(
    top_prod.melt(id_vars="PRODUCTO", value_vars=["Montajes", "Desmontajes"],
                  var_name="Tipo", value_name="Cantidad"),
    x="PRODUCTO", y="Cantidad", color="Tipo", barmode="group",
    title=f"Top {top_n} productos — montajes vs desmontajes",
)
fig.update_xaxes(tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(agg_prod.round(1), hide_index=True, use_container_width=True)

st.divider()

# ============================================================
# DETALLE Y DESCARGA
# ============================================================
with st.expander("📋 Ver detalle de operaciones filtradas"):
    st.dataframe(
        dff[["FECHA", "MONTADOR", "NOMBRE DEL MONTADOR  / LÍDER", "PRODUCTO",
             "CLIENTE", "TIPO", "TIEMPO NETO", "TIEMPO PROGRAMADO",
             "TIEMPOS PAROS/MUERTOS"]],
        hide_index=True, use_container_width=True,
    )
    st.download_button("⬇️ Descargar CSV", dff.to_csv(index=False).encode("utf-8"),
                       "operaciones_filtradas.csv", "text/csv")
