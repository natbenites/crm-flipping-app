import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Deal Flow | Flipping BA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilizado Minimalista Apple-Style
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FBFBFD;
        color: #1D1D1F;
    }
    
    /* Ocultar barra superior y ajustes generales */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Contenedor de KPIs sin cajas, dividido por líneas finas */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        padding: 24px 32px;
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.04);
        margin-bottom: 35px;
    }
    .kpi-item {
        flex: 1;
        text-align: left;
        padding: 0 20px;
        border-right: 1px solid #E5E5EA;
    }
    .kpi-item:first-child { padding-left: 0; }
    .kpi-item:last-child { border-right: none; padding-right: 0; }
    
    .kpi-label {
        font-size: 0.78em;
        font-weight: 500;
        color: #86868B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 1.8em;
        font-weight: 300;
        color: #1D1D1F;
        letter-spacing: -0.5px;
    }
    
    /* Cards de Propiedades */
    .property-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    
    .property-title {
        font-size: 1.25em;
        font-weight: 500;
        color: #000000;
        margin: 0 0 8px 0;
        letter-spacing: -0.3px;
    }
    
    .property-metrics {
        font-size: 0.9em;
        font-weight: 300;
        color: #515154;
        margin-bottom: 16px;
    }
    
    /* Tags Minimalistas Neutrales */
    .tag-flat {
        display: inline-block;
        background: #F2F2F7;
        color: #1D1D1F;
        font-size: 0.75em;
        font-weight: 500;
        padding: 3px 10px;
        border-radius: 6px;
        margin-right: 6px;
    }
    
    /* Botones compactos y elegantes */
    .stButton > button {
        border-radius: 6px;
        border: 1px solid #D2D2D7;
        color: #1D1D1F;
        background-color: #FFFFFF;
        font-size: 0.82em;
        font-weight: 400;
        padding: 4px 12px;
        height: auto;
        transition: all 0.15s ease;
    }
    .stButton > button:hover {
        border-color: #1B263B;
        color: #1B263B;
        background-color: #F5F5F7;
    }
    
    /* Custom Slider & Selectbox en Sidebar */
    .stSlider > div > div > div > div {
        background: #1B263B !important;
    }
    </style>
""", unsafe_allow_html=True)

# Cabecera Principal (Tipografía ultrafina y limpia)
st.markdown("<h1 style='font-weight: 300; font-size: 2.2em; color: #000000; margin-bottom: 2px; letter-spacing: -1px;'>Deal Flow | Flipping BA</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.95em; font-weight: 300; color: #86868B; margin-top: 0; margin-bottom: 28px;'>Propiedades Filtradas</p>", unsafe_allow_html=True)

# KPIs con División Minimalista
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
        <div class='kpi-value' style='color: #1B263B;'>-18%</div>
    </div>
    <div class='kpi-item'>
        <div class='kpi-label'>Tiempo Prom. Publicado</div>
        <div class='kpi-value'>45 días</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar (Filtros sobrios)
st.sidebar.markdown("<p style='font-size: 0.9em; font-weight: 600; color: #1D1D1F; margin-bottom: 15px;'>Filtros de Mercado</p>", unsafe_allow_html=True)
bairro = st.sidebar.multiselect("Barrios", ["Belgrano", "Palermo", "Recoleta", "Barrio Norte", "Caballito", "Villa Crespo", "Abasto", "Almagro"], default=["Palermo", "Recoleta"])
faixa_preco = st.sidebar.slider("Rango de Precio (USD)", 80000, 250000, (100000, 200000))
ambientes = st.sidebar.selectbox("Ambientes", ["Todos", "Monoambiente", "2 ambientes", "3 ambientes", "4 ambientes"])
data_pub = st.sidebar.selectbox("Fecha de Publicación", ["Cualquier fecha", "Últimos 7 días", "Últimos 15 días", "Último mes"])

# Card Propiedad 1
st.markdown("""
<div class='property-card'>
    <div style='display: flex; gap: 20px; align-items: center;'>
        <img src="https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=300&q=80" style="width: 140px; height: 95px; border-radius: 8px; object-fit: cover;">
        <div style='flex: 1;'>
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
</div>
""", unsafe_allow_html=True)

# Botones Compactos Card 1
btn_col1, btn_col2, _ = st.columns([1.2, 1.2, 3.6])
with btn_col1:
    st.button("Analizar Riesgo vs Retorno (IA)", key="ia1")
with btn_col2:
    st.button("Ver Publicación Original", key="link1")

st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# Card Propiedad 2
st.markdown("""
<div class='property-card'>
    <div style='display: flex; gap: 20px; align-items: center;'>
        <img src="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=300&q=80" style="width: 140px; height: 95px; border-radius: 8px; object-fit: cover;">
        <div style='flex: 1;'>
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
</div>
""", unsafe_allow_html=True)

# Botones Compactos Card 2
btn_col3, btn_col4, _ = st.columns([1.2, 1.2, 3.6])
with btn_col3:
    st.button("Analizar Riesgo vs Retorno (IA)", key="ia2")
with btn_col4:
    st.button("Ver Publicación Original", key="link2")
