import streamlit as st

# Configuração da página executiva
st.set_page_config(
    page_title="CRM Flipping - Buenos Aires",
    page_icon="🏢",
    layout="wide"
)

# Estilização visual (Dark Mode Executivo)
st.title("🏢 Radar de Inteligência Imobiliária & Flipping")
st.caption("Sistema de Monitoramento e Análise de Oportunidades | Buenos Aires")

st.divider()

# Indicadores de Performance (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Total Oportunidades", value="12", delta="+3 hoje")
col2.metric(label="Preço Médio m²", value="USD 1,250", delta="-8% vs Mercado")
col3.metric(label="Bairro Top Retorno", value="Palermo", delta="4 Ambientes")
col4.metric(label="Margem Média Projetada", value="USD 35,000", delta="Líquido")

st.divider()

# Área do Filtro do App
st.sidebar.header("🔍 Filtros de Mercado")
bairro = st.sidebar.multiselect("Bairros", ["Palermo", "Recoleta", "Barrio Norte", "Belgrano"], default=["Palermo", "Recoleta"])
faixa_preco = st.sidebar.slider("Faixa de Preço (USD)", 80000, 250000, (100000, 200000))
ambientes = st.sidebar.selectbox("Ambientes", ["Todos", "3 ambientes", "4 ambientes"])

# Simulação dos Cards de Imóveis (Onde a IA atua)
st.subheader("🔥 Imóveis Qualificados para Flipping")

# Card 1
with st.container():
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("### 📍 Palermo - Av. Santa Fe / Frente ao Ateneo")
        st.write("**Preço:** USD 135.000 | **Metragem:** 110m² | **Preço/m²:** USD 1.227 | **Expensas:** $ 380.000 ARS")
        st.write("🟢 **Status:** *A refaccionar | Vendedor urgente / Aceita proposta*")
    with c2:
        st.button("🤖 Gerar Proposta de IA", key="btn1")
        st.button("📲 Chamar Corretor (WhatsApp)", key="wsp1")

st.divider()

# Card 2
with st.container():
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("### 📍 Recoleta - Calle Juncal")
        st.write("**Preço:** USD 180.000 | **Metragem:** 130m² | **Preço/m²:** USD 1.384 | **Expensas:** $ 410.000 ARS")
        st.write("🟢 **Status:** *Retasado / Sucesión terminada / Listo para escriturar*")
    with c2:
        st.button("🤖 Gerar Proposta de IA", key="btn2")
        st.button("📲 Chamar Corretor (WhatsApp)", key="wsp2")
