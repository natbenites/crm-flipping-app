import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Deal Flow | Flipping BA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização estrita para limpar totalmente o sidebar e os cards
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        background-color: #FBFBFD !important;
        color: #1D1D1F !important;
    }
    
    #MainMenu, footer { visibility: hidden; }
    
    /* Remove caixas pretas das tags de bairros */
    span[data-baseweb="tag"] {
        background-color: #E5E5EA !important;
        border: none !important;
    }
    span[data-baseweb="tag"] span {
        color: #1D1D1F !important;
    }
    
    /* Remove completamente os balões pretos de valores do Slider */
    div[data-testid="stThumbValue"] {
        display: none !important;
    }
    div[aria-valuetext] {
        color: #1D1D1F !important;
    }
    .stSlider [data-baseweb="slider"] div {
        background-color: #D2D2D7 !important;
    }
    
    /* KPIs Executivos Sem Borda */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        padding: 20px 30px;
        border-radius: 10px;
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
    .kpi-item {
        flex: 1;
        text-align: left;
        padding: 0 15px;
        border-right: 1px solid #E5E5EA;
    }
    .kpi-item:last-child { border-right: none; }
    
    .kpi-label {
        font-size: 0.72em;
        font-weight: 600;
        color: #86868B;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 2px;
    }
    .kpi-value {
        font-size: 1.6em;
        font-weight: 300;
        color: #1D1D1F;
        letter-spacing: -0.5px;
    }
    
    /* Cards de Imóveis Proporcionais */
    .property-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 12px;
        display: flex;
        gap: 24px;
        align-items: center;
    }
    
    .property-img {
        width: 220px;
        height: 140px;
        border-radius: 8px;
        object-fit: cover;
        flex-shrink: 0;
    }
    
    .property-info { flex: 1; }
    
    .property-title {
        font-size: 1.15em;
        font-weight: 500;
        color: #1D1D1F;
        margin-bottom: 6px;
    }
    
    .property-metrics {
        font-size: 0.88em;
        font-weight: 300;
        color: #6E6E73;
        margin-bottom: 12px;
    }
    
    .tag-flat {
        display: inline-block;
        background: #F2F2F7;
        color: #1D1D1F;
        font-size: 0.75em;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 6px;
        margin-right: 6px;
    }
    
    /* Botões Limpos e Compactos */
    .stButton > button {
        border-radius: 6px !important;
        border: 1px solid #D2D2D7 !important;
        color: #1D1D1F !important;
        background-color: #FFFFFF !important;
        font-size: 0.8em !important;
        font-weight: 400 !important;
        padding: 4px 14px !important;
        height: 34px !important;
        width: auto !important;
    }
    .stButton > button:hover {
        border-color: #1D1D1F !important;
        color: #1D1D1F !important;
        background-color: #F5F5F7 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título Principal
st.markdown("<h1 style='font-weight: 300; font-size: 2.1em; color: #1D1D1F; margin-bottom: 2px; letter-spacing: -0.8px;'>Deal Flow | Flipping BA</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.9em; font-weight: 300; color: #86868B; margin-top: 0; margin-bottom: 25px;'>Propiedades Filtradas</p>", unsafe_allow_html=True)

# Indicadores KPIs
st.markdown("""
<div class='kpi-container'>
    <div class='kpi-item'>
        <div class='kpi-label'>Oportunidades Activas</div>
        <div class='kpi-value'>12</div>
    </div>
    <div class='kpi-item'>
        <div class='kpi-label'>Precio Promedio m²</div>
        <div class='kpi-value'>USD 1.250</div>
    </div>
    <div class='kpi-item'>
        <div class='kpi-label'>Descuento vs Mercado</div>
        <div class='kpi-value'>-18%</div>
    </div>
    <div class='kpi-item'>
        <div class='kpi-label'>Tiempo Prom. Publicado</div>
        <div class='kpi-value'>45 días</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Filtros do Menu Lateral
st.sidebar.markdown("<p style='font-size: 0.85em; font-weight: 600; color: #1D1D1F; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px;'>Filtros de Mercado</p>", unsafe_allow_html=True)
bairro = st.sidebar.multiselect("Barrios", ["Belgrano", "Palermo", "Recoleta", "Barrio Norte", "Caballito", "Villa Crespo", "Abasto", "Almagro"], default=["Palermo", "Recoleta"])

# Slider sem os números pretos sobrepostos
min_p, max_p = st.sidebar.slider("Rango de Precio (USD)", 80000, 250000, (100000, 200000))
st.sidebar.caption(f"Seleccionado: **USD {min_p:,}** a **USD {max_p:,}**")

ambientes = st.sidebar.selectbox("Ambientes", ["Todos", "Monoambiente", "2 ambientes", "3 ambientes", "4 ambientes"])
data_pub = st.sidebar.selectbox("Fecha de Publicación", ["Cualquier fecha", "Últimos 7 días", "Últimos 15 días", "Último mes"])

# Card Imóvel 1
st.markdown("""
<div class='property-card'>
    <img class='property-img' src="https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=500&q=80">
    <div class='property-info'>
        <div class='property-title'>Palermo · Av. Santa Fe</div>
        <div class='property-metrics'>
            USD 135.000 &nbsp;·&nbsp; 110 m² &nbsp;·&nbsp; USD 1.227/m² &nbsp;·&nbsp; Expensas $380.000 ARS
        </div>
        <div>
            <span class='tag-flat'>A refaccionar</span>
            <span class='tag-flat'>Sucesión</span>
            <span class='tag-flat' style='background: #E5E5EA;'>Publicado hace 62 días</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, _ = st.columns([1.1, 1.1, 4])
with col1:
    st.button("Analizar Riesgo vs Retorno (IA)", key="ia1")
with col2:
    st.button("Ver Publicación Original", key="link1")

st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# Card Imóvel 2
st.markdown("""
<div class='property-card'>
    <img class='property-img' src="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=500&q=80">
    <div class='property-info'>
        <div class='property-title'>Recoleta · Calle Juncal</div>
        <div class='property-metrics'>
            USD 180.000 &nbsp;·&nbsp; 130 m² &nbsp;·&nbsp; USD 1.384/m² &nbsp;·&nbsp; Expensas $410.000 ARS
        </div>
        <div>
            <span class='tag-flat'>Retasado</span>
            <span class='tag-flat'>Urgente</span>
            <span class='tag-flat' style='background: #E5E5EA;'>Publicado hace 28 días</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col3, col4, _ = st.columns([1.1, 1.1, 4])
with col3:
    st.button("Analizar Riesgo vs Retorno (IA)", key="ia2")
with col4:
    st.button("Ver Publicación Original", key="link2")
