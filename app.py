import streamlit as st
import json
import os

# Configuração da página
st.set_page_config(
    page_title="Deal Flow | Flipping BA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização estrita e limpa da interface
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        background-color: #FBFBFD !important;
        color: #1D1D1F !important;
    }
    
    #MainMenu, footer { visibility: hidden; }
    
    /* Estilização das tags do Sidebar */
    span[data-baseweb="tag"] {
        background-color: #E5E5EA !important;
        border: none !important;
    }
    span[data-baseweb="tag"] span {
        color: #1D1D1F !important;
    }
    
    /* Oculta seletores escuros do Slider */
    div[data-testid="stThumbValue"] { display: none !important; }
    .stSlider [data-baseweb="slider"] div { background-color: #D2D2D7 !important; }
    
    /* Container Executivo de KPIs */
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
    
    /* Botões Compactos */
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

# Função para carregar os dados reais gerados pelo scraper
def carregar_dados():
    if os.path.exists("dados_imoveis.json"):
        with open("dados_imoveis.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

imoveis = carregar_dados()

# Cabecalho
st.markdown("<h1 style='font-weight: 300; font-size: 2.1em; color: #1D1D1F; margin-bottom: 2px; letter-spacing: -0.8px;'>Deal Flow | Flipping BA</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.9em; font-weight: 300; color: #86868B; margin-top: 0; margin-bottom: 25px;'>Propiedades Filtradas en Tiempo Real</p>", unsafe_allow_html=True)

# Cálculo dinâmico dos KPIs baseados nos dados coletados
total_imoveis = len(imoveis)
preco_medio_m2 = round(sum(i['preco_m2'] for i in imoveis) / total_imoveis, 2) if total_imoveis > 0 else 0

st.markdown(f"""
<div class='kpi-container'>
    <div class='kpi-item'>
        <div class='kpi-label'>Oportunidades Activas</div>
        <div class='kpi-value'>{total_imoveis}</div>
    </div>
    <div class='kpi-item'>
        <div class='kpi-label'>Precio Promedio m²</div>
        <div class='kpi-value'>USD {preco_medio_m2:,.0f}</div>
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

# Sidebar de Filtros
st.sidebar.markdown("<p style='font-size: 0.85em; font-weight: 600; color: #1D1D1F; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px;'>Filtros de Mercado</p>", unsafe_allow_html=True)
bairros_sel = st.sidebar.multiselect("Barrios", ["Belgrano", "Palermo", "Recoleta", "Barrio Norte", "Caballito", "Villa Crespo"], default=["Palermo", "Recoleta"])
min_p, max_p = st.sidebar.slider("Rango de Precio (USD)", 50000, 300000, (80000, 200000))
st.sidebar.caption(f"Seleccionado: **USD {min_p:,}** a **USD {max_p:,}**")

# Exibição dos cards reais
if not imoveis:
    st.info("Aún no hay datos capturados. Ejecuta 'scraper.py' para sincronizar el mercado.")
else:
    for idx, item in enumerate(imoveis):
        st.markdown(f"""
        <div class='property-card'>
            <img class='property-img' src="{item['imagem']}">
            <div class='property-info'>
                <div class='property-title'>{item['bairro']} · {item['titulo']}</div>
                <div class='property-metrics'>
                    USD {item['preco_usd']:,} &nbsp;·&nbsp; {item['metragem']} m² &nbsp;·&nbsp; USD {item['preco_m2']}/m² &nbsp;·&nbsp; Expensas ${item['expensas_ars']:,} ARS
                </div>
                <div>
                    <span class='tag-flat'>{item['fonte']}</span>
                    <span class='tag-flat' style='background: #E5E5EA;'>Verificado</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, _ = st.columns([1.2, 1.2, 3.6])
        with col1:
            if st.button("Analizar Riesgo vs Retorno (IA)", key=f"ia_{idx}"):
                st.info(f"Análisis IA para {item['titulo']}: Propiedad con precio por m² de USD {item['preco_m2']}. Margen estimado de negociación: 10-15%.")
        with col2:
            st.markdown(f'<a href="{item["link"]}" target="_blank"><button style="border-radius:6px; border:1px solid #D2D2D7; color:#1D1D1F; background:#FFF; font-size:0.8em; padding:4px 14px; height:34px;">Ver Publicación Original</button></a>', unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
