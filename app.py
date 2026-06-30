import streamlit as st
import pandas as pd
import openpyxl

# 1. Configuración de la interfaz web
st.set_page_config(page_title="Dashboard Incendios 2025-2026", layout="wide", page_icon="🔥")
st.title("🔥 Panel de Control: Investigación de Incendios Forestales")
st.markdown("Temporada 2025-2026 — Análisis de Causas y Superficies")

# 2. Cargar los datos desde tu archivo Excel
@st.cache_data
def cargar_datos():
    return pd.read_excel("DATOS DUROS 2025-2026 WEB.xlsx", sheet_name="Invest. IF")

try:
    df = cargar_datos()

    # 3. Sidebar (Menú lateral) para Filtros Interactivos
    st.sidebar.header("🎯 Filtros Disponibles")
    
    regiones = ["Todas"] + list(df["Región"].unique())
    region_sel = st.sidebar.selectbox("Selecciona Región:", regiones)
    
    provincias = ["Todas"] + list(df["Provincia"].unique())
    provincia_sel = st.sidebar.selectbox("Selecciona Provincia:", provincias)
    
    grupos = ["Todos"] + list(df["Grupo de causas"].unique())
    grupo_sel = st.sidebar.selectbox("Grupo de Causas:", grupos)

    # 4. Lógica de filtrado dinámico
    df_filtrado = df.copy()
    if region_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Región"] == region_sel]
    if provincia_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Provincia"] == provincia_sel]
    if grupo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Grupo de causas"] == grupo_sel]

    # 5. Despliegue de Métricas en Pantalla
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="🚨 Total Incendios Investigados", value=f"{len(df_filtrado)}")
    with m2:
        total_sup = df_filtrado["Sup"].sum()
        st.metric(label="📐 Superficie Afectada Total", value=f"{total_sup:,.1f} Ha")
    with m3:
        causa_top = df_filtrado["Causa General"].mode()[0] if not df_filtrado.empty else "N/A"
        st.metric(label="⚠️ Causa General más Frecuente", value=causa_top)

    st.markdown("---")

    # 6. Gráficos Interactivos NATIVOS
    st.subheader("📊 Superficie Afectada por Causa General")
    df_causas_sup = df_filtrado.groupby("Causa General")["Sup"].sum().sort_values(ascending=False)
    st.bar_chart(df_causas_sup)

    st.markdown("---")

    # 7. Tabla Interactiva Completa
    st.subheader("📋 Registros de Incendios Filtrados")
    columnas_vista = ["ID", "Temporada", "Región", "Provincia", "Comuna", "Nombre incendio", "Causa General", "Grupo de causas", "Sup", "INICIO INCENDIO"]
    st.dataframe(df_filtrado[columnas_vista], use_container_width=True, hide_index=True)

except FileNotFoundError:
    st.error("⚠️ El archivo **'DATOS DUROS 2025-2026 WEB.xlsx'** no se encuentra en esta ruta.")
except Exception as e:
    st.error(f"❌ Ocurrió un error al procesar el archivo: {e}")
