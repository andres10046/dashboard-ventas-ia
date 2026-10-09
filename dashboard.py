import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="Dashboard Ventas 2024-2026 | Analítica con IA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS PERSONALIZADO - Estilo Infografía Moderna
# ============================================================
st.markdown("""
<style>
    .main {background-color: #f0f4f8;}
    
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 20px 15px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 6px solid #1f4e79;
        transition: transform 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    div[data-testid="stMetricValue"] {
        color: #1f4e79;
        font-size: 1.9rem;
        font-weight: 800;
    }
    div[data-testid="stMetricLabel"] {
        color: #666;
        font-size: 0.95rem;
        font-weight: 600;
    }
    
    h1 {color: #1f4e79; font-weight: 800; text-align: center;}
    h2 {
        color: #1f4e79; 
        border-bottom: 3px solid #1f4e79; 
        padding-bottom: 10px;
        margin-top: 30px;
    }
    h3 {color: #2c5f8d; font-size: 1.1rem;}
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0f4f8 100%);
        border-right: 2px solid #d0dce8;
    }
    
    div[data-testid="stPlotlyChart"] {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    
    .conclusion-box {
        background: linear-gradient(135deg, #1f4e79 0%, #2c5f8d 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-top: 30px;
        box-shadow: 0 6px 20px rgba(31,78,121,0.3);
    }
    .conclusion-box h3 {color: #7fd1ff; margin-top: 0;}
    .conclusion-box p {font-size: 1.05rem; line-height: 1.6;}
    
    .pregunta-badge {
        display: inline-block;
        background: #1f4e79;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CARGA DE DATOS
# ============================================================
@st.cache_data
def cargar_datos():
    df = pd.read_excel("ventas_globales_2024_2026.xlsx")
    df["Fecha_Venta"] = pd.to_datetime(df["Fecha_Venta"])
    return df

df = cargar_datos()

# ============================================================
# GENERADOR DE NOMBRES SINTÉTICOS DE CLIENTES
# ============================================================
nombres = ["Carlos", "María", "Juan", "Ana", "Luis", "Sofía", "Pedro", "Laura", 
           "Diego", "Carmen", "Javier", "Elena", "Andrés", "Patricia", "Roberto",
           "Isabel", "Fernando", "Gabriela", "Ricardo", "Valentina", "Miguel",
           "Daniela", "Alejandro", "Camila", "Santiago", "Lucía", "Mateo", "Emma",
           "Lucas", "Martina", "Sebastián", "Victoria", "Nicolás", "Renata"]

apellidos = ["García", "Rodríguez", "Martínez", "López", "González", "Pérez", 
             "Sánchez", "Ramírez", "Torres", "Flores", "Rivera", "Gómez", 
             "Díaz", "Cruz", "Morales", "Ortiz", "Gutiérrez", "Chávez", 
             "Ramos", "Ruiz", "Álvarez", "Castillo", "Jiménez", "Vargas"]

def id_a_nombre(cliente_id):
    """Convierte un ID como CLI-00738 en un nombre realista y consistente."""
    hash_val = int(hashlib.md5(str(cliente_id).encode()).hexdigest(), 16)
    nombre = nombres[hash_val % len(nombres)]
    apellido = apellidos[(hash_val // 100) % len(apellidos)]
    return f"{nombre} {apellido}"

# ============================================================
# BARRA LATERAL - FILTROS
# ============================================================
st.sidebar.markdown("# 🎛️ Panel de Control")
st.sidebar.markdown("Filtra los datos para explorar la información.")
st.sidebar.markdown("---")

fecha_min = df["Fecha_Venta"].min().date()
fecha_max = df["Fecha_Venta"].max().date()
rango_fechas = st.sidebar.date_input(
    "📅 Rango de fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

años = st.sidebar.multiselect(
    "📆 Año",
    options=sorted(df["Año"].unique()),
    default=sorted(df["Año"].unique())
)

regiones = st.sidebar.multiselect(
    "🌎 Región",
    options=sorted(df["Región"].unique()),
    default=sorted(df["Región"].unique())
)

categorias = st.sidebar.multiselect(
    "📦 Categoría",
    options=sorted(df["Categoría"].unique()),
    default=sorted(df["Categoría"].unique())
)

canales = st.sidebar.multiselect(
    "🛒 Canal de Venta",
    options=sorted(df["Canal_Venta"].unique()),
    default=sorted(df["Canal_Venta"].unique())
)

segmentos = st.sidebar.multiselect(
    "👥 Segmento de Cliente",
    options=sorted(df["Segmento_Cliente"].unique()),
    default=sorted(df["Segmento_Cliente"].unique())
)

st.sidebar.markdown("---")
st.sidebar.metric("📊 Registros Filtrados", f"{len(df):,}")

# ============================================================
# APLICAR FILTROS
# ============================================================
df_f = df[
    (df["Fecha_Venta"].dt.date >= rango_fechas[0]) &
    (df["Fecha_Venta"].dt.date <= rango_fechas[1]) &
    (df["Año"].isin(años)) &
    (df["Región"].isin(regiones)) &
    (df["Categoría"].isin(categorias)) &
    (df["Canal_Venta"].isin(canales)) &
    (df["Segmento_Cliente"].isin(segmentos))
]

# ============================================================
# ENCABEZADO
# ============================================================
st.title("📊 Dashboard de Ventas Globales 2024-2026")
st.markdown(f"<p style='text-align:center; color:#666; font-size:1.1rem;'>Analizando <b>{len(df_f):,}</b> transacciones | Proyecto Final - Analítica Descriptiva con IA</p>", unsafe_allow_html=True)

# ============================================================
# PREGUNTA 1
# ============================================================
st.markdown("## 1️⃣ Evolución del Desempeño Comercial")
st.markdown("<span class='pregunta-badge'>❓ ¿Cómo ha evolucionado el desempeño en ventas, utilidad y margen?</span>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Ventas Totales (USD)", f"${df_f['Venta_Neta_USD'].sum():,.0f}")
with col2:
    st.metric("📈 Utilidad Total (USD)", f"${df_f['Utilidad_USD'].sum():,.0f}")
with col3:
    margen_prom = (df_f["Utilidad_USD"].sum() / df_f["Venta_Neta_USD"].sum() * 100) if df_f["Venta_Neta_USD"].sum() > 0 else 0
    st.metric("🎯 Margen Promedio", f"{margen_prom:.1f}%")
with col4:
    st.metric("📦 Pedidos Únicos", f"{df_f['ID_Pedido'].nunique():,}")

if not df_f.empty:
    df_mes = df_f.groupby(df_f["Fecha_Venta"].dt.to_period("M")).agg({
        "Venta_Neta_USD": "sum",
        "Utilidad_USD": "sum"
    }).reset_index()
    df_mes["Fecha_Venta"] = df_mes["Fecha_Venta"].astype(str)

    fig_tiempo = go.Figure()
    fig_tiempo.add_trace(go.Scatter(
        x=df_mes["Fecha_Venta"], y=df_mes["Venta_Neta_USD"],
        name="Ventas USD", mode="lines+markers",
        line=dict(color="#1f4e79", width=3),
        fill="tozeroy", fillcolor="rgba(31,78,121,0.1)"
    ))
    fig_tiempo.add_trace(go.Scatter(
        x=df_mes["Fecha_Venta"], y=df_mes["Utilidad_USD"],
        name="Utilidad USD", mode="lines+markers",
        line=dict(color="#00a86b", width=3)
    ))
    fig_tiempo.update_layout(
        title=dict(text="📈 Evolución Mensual: Ventas vs Utilidad", y=0.97, x=0.5, xanchor='center'),
        hovermode="x unified",
        yaxis=dict(title="USD"),
        height=450,
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", y=1.12, x=0),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    st.plotly_chart(fig_tiempo, use_container_width=True)

st.markdown("---")

# ============================================================
# PREGUNTA 2
# ============================================================
st.markdown("## 2️⃣ Análisis Geográfico: Regiones, Países y Ciudades")
st.markdown("<span class='pregunta-badge'>❓ ¿Qué regiones generan más ventas y cuáles mayor rentabilidad?</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    df_reg = df_f.groupby("Región").agg({
        "Venta_Neta_USD": "sum",
        "Utilidad_USD": "sum"
    }).reset_index()
    df_reg["Margen"] = (df_reg["Utilidad_USD"] / df_reg["Venta_Neta_USD"]) * 100
    df_reg = df_reg.sort_values("Venta_Neta_USD", ascending=True)

    fig_reg = px.bar(
        df_reg, x="Venta_Neta_USD", y="Región", orientation="h",
        color="Margen", color_continuous_scale="Blues",
        text="Venta_Neta_USD",
        title="🌎 Ventas y Margen por Región"
    )
    fig_reg.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig_reg.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        coloraxis_colorbar=dict(title="Margen %"),
        margin=dict(l=10, r=80, t=70, b=10),
        xaxis_title="Ventas USD", yaxis_title=""
    )
    st.plotly_chart(fig_reg, use_container_width=True)

with col2:
    df_pais = df_f.groupby("País")["Venta_Neta_USD"].sum().nlargest(10).reset_index()
    fig_pais = px.bar(
        df_pais, x="País", y="Venta_Neta_USD",
        color="Venta_Neta_USD", color_continuous_scale="Teal",
        title="🌍 Top 10 Países por Ventas"
    )
    fig_pais.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=70, b=10),
        xaxis_title="", yaxis_title="Ventas USD"
    )
    st.plotly_chart(fig_pais, use_container_width=True)

st.markdown("---")

# ============================================================
# PREGUNTA 3
# ============================================================
st.markdown("## 3️⃣ Categorías, Subcategorías y Productos")
st.markdown("<span class='pregunta-badge'>❓ ¿Qué categorías y productos explican el desempeño global?</span>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    df_cat = df_f.groupby("Categoría")["Venta_Neta_USD"].sum().sort_values(ascending=True).reset_index()
    fig_cat = px.bar(
        df_cat, x="Venta_Neta_USD", y="Categoría", orientation="h",
        color="Venta_Neta_USD", color_continuous_scale="Purples",
        title="📦 Ventas por Categoría"
    )
    fig_cat.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, coloraxis_showscale=False,
        margin=dict(l=10, r=40, t=70, b=10),
        xaxis_title="Ventas USD", yaxis_title=""
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col2:
    df_prod = df_f.groupby("Producto")["Venta_Neta_USD"].sum().nlargest(10).sort_values().reset_index()
    fig_prod = px.bar(
        df_prod, x="Venta_Neta_USD", y="Producto", orientation="h",
        color="Venta_Neta_USD", color_continuous_scale="Blugrn",
        title="🥇 Top 10 Productos"
    )
    fig_prod.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, coloraxis_showscale=False,
        margin=dict(l=10, r=40, t=70, b=10),
        xaxis_title="Ventas USD", yaxis_title=""
    )
    st.plotly_chart(fig_prod, use_container_width=True)

st.markdown("---")

# ============================================================
# PREGUNTA 4
# ============================================================
st.markdown("## 4️⃣ Relación entre Ventas y Rentabilidad")
st.markdown("<span class='pregunta-badge'>❓ ¿Existe relación entre mayores ventas y mayor rentabilidad?</span>", unsafe_allow_html=True)

if not df_f.empty:
    df_scatter = df_f.groupby(["Región", "Categoría"]).agg({
        "Venta_Neta_USD": "sum",
        "Utilidad_USD": "sum"
    }).reset_index()
    df_scatter["Margen_Porc"] = (df_scatter["Utilidad_USD"] / df_scatter["Venta_Neta_USD"]) * 100

    fig_scat = px.scatter(
        df_scatter, x="Venta_Neta_USD", y="Margen_Porc",
        color="Región", size="Venta_Neta_USD",
        hover_data=["Categoría"], size_max=60,
        title="🎯 Ventas vs Margen por Región y Categoría"
    )
    fig_scat.add_hline(y=df_scatter["Margen_Porc"].mean(), line_dash="dash", 
                       line_color="red", annotation_text="Margen Promedio")
    fig_scat.update_layout(
        height=520, plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=70, b=10),
        xaxis_title="Ventas USD", yaxis_title="Margen %",
        legend=dict(orientation="h", y=-0.15)
    )
    st.plotly_chart(fig_scat, use_container_width=True)
    st.info("💡 **Interpretación:** Los puntos en la parte inferior derecha representan regiones/categorías con **altas ventas pero márgenes bajos** (oportunidad de mejora). Los puntos arriba a la izquierda tienen **altos márgenes pero bajas ventas** (potencial de crecimiento).")

st.markdown("---")

# ============================================================
# PREGUNTA 5
# ============================================================
st.markdown("## 5️⃣ Clientes, Segmentos e Industrias de Mayor Valor")
st.markdown("<span class='pregunta-badge'>❓ ¿Qué tipos de clientes y segmentos representan mayor valor?</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    df_seg = df_f.groupby("Segmento_Cliente")["Venta_Neta_USD"].sum().reset_index()
    fig_seg = px.pie(
        df_seg, values="Venta_Neta_USD", names="Segmento_Cliente",
        hole=0.5, title="👥 Ventas por Segmento de Cliente",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_seg.update_traces(textposition="inside", textinfo="percent+label")
    fig_seg.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=70, b=10)
    )
    st.plotly_chart(fig_seg, use_container_width=True)

with col2:
    df_ind = df_f.groupby("Industria")["Venta_Neta_USD"].sum().nlargest(8).sort_values().reset_index()
    fig_ind = px.bar(
        df_ind, x="Venta_Neta_USD", y="Industria", orientation="h",
        color="Venta_Neta_USD", color_continuous_scale="Oranges",
        title="🏭 Top Industrias por Ventas"
    )
    fig_ind.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, coloraxis_showscale=False,
        margin=dict(l=10, r=40, t=70, b=10),
        xaxis_title="Ventas USD", yaxis_title=""
    )
    st.plotly_chart(fig_ind, use_container_width=True)

st.markdown("---")

# ============================================================
# PREGUNTA 6
# ============================================================
st.markdown("## 6️⃣ Canales de Venta")
st.markdown("<span class='pregunta-badge'>❓ ¿Qué canales presentan el mejor comportamiento comercial y financiero?</span>", unsafe_allow_html=True)

df_canal = df_f.groupby("Canal_Venta").agg({
    "Venta_Neta_USD": "sum",
    "Utilidad_USD": "sum"
}).reset_index()
df_canal["Margen"] = (df_canal["Utilidad_USD"] / df_canal["Venta_Neta_USD"]) * 100

col1, col2 = st.columns(2)

with col1:
    fig_canal = px.pie(
        df_canal, values="Venta_Neta_USD", names="Canal_Venta",
        hole=0.5, title="🛒 Distribución de Ventas por Canal",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_canal.update_traces(textposition="inside", textinfo="percent+label")
    fig_canal.update_layout(height=420, margin=dict(t=70))
    st.plotly_chart(fig_canal, use_container_width=True)

with col2:
    fig_canal_margen = px.bar(
        df_canal, x="Canal_Venta", y="Margen",
        color="Margen", color_continuous_scale="RdYlGn",
        title="💹 Margen % por Canal",
        text="Margen"
    )
    fig_canal_margen.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_canal_margen.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, coloraxis_showscale=False,
        margin=dict(t=70),
        xaxis_title="", yaxis_title="Margen %"
    )
    st.plotly_chart(fig_canal_margen, use_container_width=True)

st.markdown("---")

# ============================================================
# PREGUNTA 7 - CORREGIDA
# ============================================================
st.markdown("## 7️⃣ Efecto de los Descuentos")
st.markdown("<span class='pregunta-badge'>❓ ¿Qué efecto tienen los descuentos sobre ventas, utilidad y margen?</span>", unsafe_allow_html=True)

if not df_f.empty:
    df_desc = df_f.groupby(df_f["Fecha_Venta"].dt.to_period("M")).agg({
        "Descuento_Porc": "mean",
        "Venta_Neta_USD": "sum",
        "Utilidad_USD": "sum"
    }).reset_index()
    df_desc["Fecha_Venta"] = df_desc["Fecha_Venta"].astype(str)
    df_desc["Descuento_Porc"] = df_desc["Descuento_Porc"] * 100

    fig_desc = make_subplots(specs=[[{"secondary_y": True}]])
    fig_desc.add_trace(
        go.Bar(x=df_desc["Fecha_Venta"], y=df_desc["Descuento_Porc"],
               name="Descuento %", marker_color="#f39c12", opacity=0.7),
        secondary_y=False
    )
    fig_desc.add_trace(
        go.Scatter(x=df_desc["Fecha_Venta"], y=df_desc["Utilidad_USD"],
                   name="Utilidad USD", mode="lines+markers",
                   line=dict(color="#1f4e79", width=3)),
        secondary_y=True
    )
    fig_desc.update_layout(
        title=dict(
            text="💸 Descuento Promedio vs Utilidad Mensual",
            y=0.97, x=0.5, xanchor='center', yanchor='top',
            font=dict(size=18, color="#1f4e79")
        ),
        hovermode="x unified",
        height=480,
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", y=1.12, x=0),
        margin=dict(t=100, b=40, l=40, r=40)
    )
    fig_desc.update_yaxes(title_text="Descuento %", secondary_y=False)
    fig_desc.update_yaxes(title_text="Utilidad USD", secondary_y=True)
    st.plotly_chart(fig_desc, use_container_width=True)
    
    # Interpretación dinámica
    desc_prom = df_desc["Descuento_Porc"].mean()
    correlacion = df_desc["Descuento_Porc"].corr(df_desc["Utilidad_USD"])
    if correlacion < -0.3:
        conclusion = "existe una **correlación negativa fuerte**: a mayor descuento, menor utilidad"
    elif correlacion < 0:
        conclusion = "existe una **correlación negativa leve**: los descuentos altos tienden a reducir la utilidad"
    else:
        conclusion = "no hay una relación clara entre descuento y utilidad en el período"
    
    st.info(f"""
    💡 **Interpretación:** El descuento promedio otorgado es del **{desc_prom:.1f}%**. 
    Con base en los datos mensuales, {conclusion}. Se recomienda revisar la política de descuentos en las 
    categorías con márgenes ajustados para no comprometer la rentabilidad del negocio.
    """)

st.markdown("---")

# ============================================================
# PREGUNTA 8
# ============================================================
st.markdown("## 8️⃣ Desempeño de Vendedores y Equipos")
st.markdown("<span class='pregunta-badge'>❓ ¿Cómo se compara el desempeño de vendedores y equipos comerciales?</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    df_eq = df_f.groupby("Equipo_Comercial").agg({
        "Venta_Neta_USD": "sum",
        "Utilidad_USD": "sum"
    }).reset_index()
    df_eq["Margen"] = (df_eq["Utilidad_USD"] / df_eq["Venta_Neta_USD"]) * 100
    df_eq = df_eq.sort_values("Venta_Neta_USD", ascending=True)

    fig_eq = px.bar(
        df_eq, x="Venta_Neta_USD", y="Equipo_Comercial", orientation="h",
        color="Margen", color_continuous_scale="Viridis",
        title="🏅 Ventas por Equipo Comercial"
    )
    fig_eq.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        coloraxis_colorbar=dict(title="Margen %"),
        margin=dict(l=10, r=60, t=70, b=10),
        xaxis_title="Ventas USD", yaxis_title=""
    )
    st.plotly_chart(fig_eq, use_container_width=True)

with col2:
    df_vend = df_f.groupby("Vendedor")["Venta_Neta_USD"].sum().nlargest(10).sort_values().reset_index()
    fig_vend = px.bar(
        df_vend, x="Venta_Neta_USD", y="Vendedor", orientation="h",
        color="Venta_Neta_USD", color_continuous_scale="Cividis",
        title="🥇 Top 10 Vendedores"
    )
    fig_vend.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, coloraxis_showscale=False,
        margin=dict(l=10, r=40, t=70, b=10),
        xaxis_title="Ventas USD", yaxis_title=""
    )
    st.plotly_chart(fig_vend, use_container_width=True)

st.markdown("---")

# ============================================================
# PREGUNTA 9 - CON NOMBRES DE CLIENTES
# ============================================================
st.markdown("## 9️⃣ Concentración y Recurrencia de Clientes")
st.markdown("<span class='pregunta-badge'>❓ ¿Qué tan concentradas están las ventas en determinados clientes?</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    df_top_cli = df_f.groupby("ID_Cliente").agg({
        "Venta_Neta_USD": "sum",
        "ID_Pedido": "nunique"
    }).reset_index().nlargest(15, "Venta_Neta_USD")
    df_top_cli.columns = ["Cliente_ID", "Ventas", "Pedidos"]
    df_top_cli["Cliente"] = df_top_cli["Cliente_ID"].apply(id_a_nombre)
    df_top_cli["Etiqueta"] = df_top_cli["Cliente"] + " (" + df_top_cli["Cliente_ID"] + ")"

    fig_cli = px.bar(
        df_top_cli.sort_values("Ventas"), 
        x="Ventas", 
        y="Etiqueta", 
        orientation="h",
        color="Ventas", 
        color_continuous_scale="Reds",
        title="👑 Top 15 Clientes por Ventas"
    )
    fig_cli.update_layout(
        height=520, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, coloraxis_showscale=False,
        margin=dict(l=10, r=40, t=70, b=10),
        xaxis_title="Ventas USD", yaxis_title=""
    )
    st.plotly_chart(fig_cli, use_container_width=True)

with col2:
    total_ventas = df_f["Venta_Neta_USD"].sum()
    top10_ventas = df_top_cli.head(10)["Ventas"].sum()
    concentracion = (top10_ventas / total_ventas * 100) if total_ventas > 0 else 0

    st.metric("🎯 Concentración Top 10 Clientes", f"{concentracion:.1f}%",
              help="Porcentaje de las ventas totales generadas por los 10 principales clientes")
    
    df_recurrencia = df_f.groupby("ID_Cliente")["ID_Pedido"].nunique().reset_index()
    df_recurrencia.columns = ["Cliente", "Num_Pedidos"]

    fig_rec = px.histogram(
        df_recurrencia, x="Num_Pedidos", nbins=20,
        title="🔄 Distribución de Recurrencia de Clientes",
        color_discrete_sequence=["#1f4e79"]
    )
    fig_rec.update_layout(
        height=380, plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=70),
        xaxis_title="Número de Pedidos", yaxis_title="Cantidad de Clientes"
    )
    st.plotly_chart(fig_rec, use_container_width=True)

if not df_f.empty:
    total_v = df_f["Venta_Neta_USD"].sum()
    top10_v = df_f.groupby("ID_Cliente")["Venta_Neta_USD"].sum().nlargest(10).sum()
    conc_actual = (top10_v / total_v * 100) if total_v > 0 else 0
    rec_prom = df_f.groupby("ID_Cliente")["ID_Pedido"].nunique().mean()
    
    if conc_actual > 30:
        nivel_conc = "**alta concentración** (riesgo si se pierde un cliente clave)"
    elif conc_actual > 15:
        nivel_conc = "**concentración moderada** (cartera relativamente equilibrada)"
    else:
        nivel_conc = "**baja concentración** (cartera muy diversificada)"

    st.info(f"""
    💡 **Interpretación:** Los 10 principales clientes generan el **{conc_actual:.1f}%** de las ventas totales, 
    lo que indica una **{nivel_conc}**. Además, cada cliente realiza en promedio **{rec_prom:.1f} pedidos**, 
    lo que refleja el nivel de recurrencia. Si la concentración es superior al 30%, se recomienda **diversificar 
    la cartera** para reducir el riesgo comercial.
    """)

st.markdown("---")

# ============================================================
# PREGUNTA 10
# ============================================================
st.markdown("## 🔟 Entrega de Pedidos: Oportunidades de Mejora")
st.markdown("<span class='pregunta-badge'>❓ ¿Dónde existen oportunidades de mejora en la entrega de pedidos?</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig_box = px.box(
        df_f, x="Estado_Pedido", y="Dias_Entrega",
        color="Estado_Pedido",
        title="🚚 Días de Entrega por Estado del Pedido",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_box.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, margin=dict(t=70),
        xaxis_title="", yaxis_title="Días"
    )
    st.plotly_chart(fig_box, use_container_width=True)

with col2:
    df_metodo = df_f.groupby("Metodo_Pago")["Dias_Entrega"].mean().sort_values().reset_index()
    fig_metodo = px.bar(
        df_metodo, x="Dias_Entrega", y="Metodo_Pago", orientation="h",
        color="Dias_Entrega", color_continuous_scale="RdYlGn_r",
        title="💳 Días Promedio de Entrega por Método de Pago",
        text="Dias_Entrega"
    )
    fig_metodo.update_traces(texttemplate="%{text:.1f} días", textposition="outside")
    fig_metodo.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, coloraxis_showscale=False,
        margin=dict(l=10, r=80, t=70, b=10),
        xaxis_title="Días promedio", yaxis_title=""
    )
    st.plotly_chart(fig_metodo, use_container_width=True)

if not df_f.empty:
    dias_prom = df_f["Dias_Entrega"].mean()
    dias_max = df_f["Dias_Entrega"].max()
    estado_lento = df_f.groupby("Estado_Pedido")["Dias_Entrega"].mean().idxmax()
    estado_rapido = df_f.groupby("Estado_Pedido")["Dias_Entrega"].mean().idxmin()
    metodo_lento = df_f.groupby("Metodo_Pago")["Dias_Entrega"].mean().idxmax()
    
    pedidos_lentos = len(df_f[df_f["Dias_Entrega"] > dias_prom + 5])
    porc_lentos = (pedidos_lentos / len(df_f) * 100)

    st.info(f"""
    💡 **Interpretación:** El tiempo promedio de entrega es de **{dias_prom:.1f} días**, 
    con un máximo de **{dias_max} días**. Los pedidos en estado **'{estado_lento}'** son los más lentos 
    (promedio más alto), mientras que **'{estado_rapido}'** es el más ágil. El método de pago 
    **'{metodo_lento}'** está asociado a los mayores tiempos de entrega. 
    El **{porc_lentos:.1f}%** de los pedidos supera el promedio en más de 5 días, lo que representa una 
    **oportunidad de mejora logística** prioritaria. Se recomienda revisar los procesos de los pedidos 
    pendientes y optimizar la operación con los métodos de pago más lentos.
    """)

# ============================================================
# CONCLUSIÓN FINAL
# ============================================================
if not df_f.empty:
    st.markdown("---")
    st.markdown(f"""
    <div class='conclusion-box'>
        <h3>💡 Conclusión del Análisis</h3>
        <p>Con base en los <b>{len(df_f):,}</b> registros analizados con los filtros aplicados:</p>
        <ul>
            <li>Las <b>ventas totales</b> alcanzan <b>${df_f['Venta_Neta_USD'].sum():,.0f} USD</b> con una utilidad de <b>${df_f['Utilidad_USD'].sum():,.0f} USD</b>.</li>
            <li>El <b>margen promedio global</b> es del <b>{margen_prom:.1f}%</b>, lo que indica una operación rentable.</li>
            <li>La región líder en ventas es <b>{df_f.groupby('Región')['Venta_Neta_USD'].sum().idxmax()}</b>, mientras que <b>{df_f.groupby('Categoría')['Venta_Neta_USD'].sum().idxmax()}</b> es la categoría más destacada.</li>
            <li>La operación logística muestra oportunidades de mejora en los pedidos pendientes.</li>
        </ul>
        <p style='margin-bottom:0;'>
            <b>Recomendación:</b> Enfocar los esfuerzos comerciales en las regiones con alto margen y bajo volumen, 
            optimizar la política de descuentos y mejorar los tiempos de entrega.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("📊 Dashboard creado con Streamlit + Plotly | Proyecto Final - Analítica Descriptiva con IA")