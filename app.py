import streamlit as st

# Configuración de la página (layout expandido)
st.set_page_config(
    page_title="Deal Flow | Flipping BA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Personalizado (Estética corporativa clara, sem ícones)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8F9FA; /* Fundo cinza claríssimo */
        color: #2D3142; /* Cinza chumbo para textos */
    }
    
    /* Ajuste da cor do slider (Azul Marinho) */
    .stSlider > div > div > div > div {
        background: #1B263B !important; 
    }
    
    /* Ajuste visual dos botões */
    .stButton > button {
        border-radius: 4px;
        border: 1px solid #1B263B;
        color: #1B263B;
        background-color: transparent;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #1B263B;
        color: #FFFFFF;
        border: 1px solid #1B263B;
    }
    
    /* Layout dos Cards e KPIs */
    .kpi-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 6px;
        border: 1px solid #EAEAEA;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .card-box {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 6px;
        border: 1px solid #EAEAEA;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    /* Etiquetas sutis */
    .tag {
        background-color: #F0F2F5;
        color: #4F5D75;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: 600;
        margin-right: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Principal
st.markdown("<h1 style='font-weight: 600; color: #1B263B; margin-bottom: 0;'>Deal Flow | Flipping BA</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.1em; color: #6C757D; margin-top: 0; margin-bottom: 30px;'>Propiedades Filtradas</p>", unsafe_allow_html=True)

# KPIs Executivos
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='kpi-box'><div style='font-size: 0.85em; color: #6C757D; text-transform: uppercase;'>Oportunidades Activas</div><div style='font-size: 1.8em; font-weight: 600;'>12</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='kpi-box'><div style='font-size: 0.85em; color: #6C757D; text-transform: uppercase;'>Precio Promedio m²</div><div style='font-size: 1.8em; font-weight: 600;'>USD 1.250</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='kpi-box'><div style='font-size: 0.85em; color: #6C757D; text-transform: uppercase;'>Descuento vs Mercado</div><div style='font-size: 1.8em; font-weight: 600; color: #1B263B;'>-18%</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='kpi-box'><div style='font-size: 0.85em; color: #6C757D; text-transform: uppercase;'>Tiempo Prom. Publicado</div><div style='font-size: 1.8em; font-weight: 600;'>45 días</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Filtros (Sidebar)
st.sidebar.markdown("<h3 style='color: #1B263B; margin-bottom: 20px;'>Filtros de Mercado</h3>", unsafe_allow_html=True)
bairro = st.sidebar.multiselect("Barrios", ["Belgrano", "Palermo", "Recoleta", "Barrio Norte", "Caballito", "Villa Crespo", "Abasto", "Almagro"], default=["Palermo", "Recoleta"])
faixa_preco = st.sidebar.slider("Rango de Precio (USD)", 80000, 250000, (100000, 200000))
ambientes = st.sidebar.selectbox("Ambientes", ["Todos", "Monoambiente", "2 ambientes", "3 ambientes", "4 ambientes"])
data_pub = st.sidebar.selectbox("Fecha de Publicación", ["Cualquier fecha", "Últimos 7 días", "Últimos 15 días", "Último mes"])

# Simulação do Card 1 (Com foto integrada)
st.markdown("""
<div class='card-box'>
    <div style='display: flex; gap: 24px; align-items: flex-start;'>
        <div style='flex: 0 0 220px;'>
            <img src="https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=400&q=80" style="width: 100%; height: 160px; border-radius: 4px; object-fit: cover;">
        </div>
        <div style='flex: 1;'>
            <h3 style='margin-top: 0; margin-bottom: 12px; font-size: 1.4em; color: #1B263B;'>Palermo - Av. Santa Fe</h3>
            <p style='margin: 0 0 16px 0; color: #4F5D75; font-size: 0.95em;'>
                <strong>Precio:</strong> USD 135.000 &nbsp;|&nbsp; 
                <strong>Superficie:</strong> 110m² &nbsp;|&nbsp; 
                <strong>Precio/m²:</strong> USD 1.227 &nbsp;|&nbsp; 
                <strong>Expensas:</strong> $ 380.000 ARS
            </p>
            <div style='margin-bottom: 16px;'>
                <span class='tag'>A refaccionar</span>
                <span class='tag'>Sucesión</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Botões de Ação do Card 1
c1, c2, c3 = st.columns([1.5, 1.5, 3])
with c1:
    st.button("Analizar Riesgo vs Retorno (IA)", key="ia1", use_container_width=True)
with c2:
    st.button("Ver Publicación Original", key="link1", use_container_width=True)

st.markdown("<hr style='border: none; border-top: 1px solid #EAEAEA; margin: 30px 0;'>", unsafe_allow_html=True)

# Simulação do Card 2
st.markdown("""
<div class='card-box'>
    <div style='display: flex; gap: 24px; align-items: flex-start;'>
        <div style='flex: 0 0 220px;'>
            <img src="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=400&q=80" style="width: 100%; height: 160px; border-radius: 4px; object-fit: cover;">
        </div>
        <div style='flex: 1;'>
            <h3 style='margin-top: 0; margin-bottom: 12px; font-size: 1.4em; color: #1B263B;'>Recoleta - Calle Juncal</h3>
            <p style='margin: 0 0 16px 0; color: #4F5D75; font-size: 0.95em;'>
                <strong>Precio:</strong> USD 180.000 &nbsp;|&nbsp; 
                <strong>Superficie:</strong> 130m² &nbsp;|&nbsp; 
                <strong>Precio/m²:</strong> USD 1.384 &nbsp;|&nbsp; 
                <strong>Expensas:</strong> $ 410.000 ARS
            </p>
            <div style='margin-bottom: 16px;'>
                <span class='tag'>Retasado</span>
                <span class='tag'>Urgente</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Botões de Ação do Card 2
c4, c5, c6 = st.columns([1.5, 1.5, 3])
with c4:
    st.button("Analizar Riesgo vs Retorno (IA)", key="ia2", use_container_width=True)
with c5:
    st.button("Ver Publicación Original", key="link2", use_container_width=True)
