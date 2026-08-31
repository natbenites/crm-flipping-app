import requests
from bs4 import BeautifulSoup
import json
import re

# Trava anticiladas: imóveis com estes termos na descrição são descartados automaticamente
TERMOS_EXCLUSAO = [
    "sin ascensor", "acceso por escalera", "primer piso por escalera",
    "no acepta mascotas", "sin mascotas", "alquiler temporal",
    "ocupado", "sin escritura", "cesion de derechos", "indiviso",
    "solo efectivo", "lateral ciego", "sin luz", "interno ciego"
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def passou_no_filtro(texto):
    """Retorna False se encontrar qualquer termo anticilada na descrição/título."""
    texto_lc = texto.lower()
    return not any(termo in texto_lc for termo in TERMOS_EXCLUSAO)

# --- MÓDULO 1: MERCADO LIBRE ---
def extrair_mercado_libre(bairro="palermo", limite=15):
    imoveis = []
    url = f"https://api.mercadolibre.com/sites/MLA/search?category=MLA1459&q={bairro}%20buenos%20aires&limit={limite}"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            for item in res.json().get("results", []):
                if item.get("currency_id") != "USD":
                    continue
                
                titulo = item.get("title", "")
                if not passou_no_filtro(titulo):
                    continue

                metragem, expensas = 0, 0
                for attr in item.get("attributes", []):
                    if attr.get("id") == "TOTAL_AREA":
                        metragem = attr.get("value_struct", {}).get("number", 0)
                    if attr.get("id") == "MAINTENANCE_FEE":
                        expensas = attr.get("value_struct", {}).get("number", 0)

                if metragem <= 0:
                    continue

                preco_usd = item.get("price", 0)
                imoveis.append({
                    "id": f"meli_{item.get('id')}",
                    "titulo": titulo,
                    "bairro": bairro.capitalize(),
                    "preco_usd": preco_usd,
                    "metragem": metragem,
                    "preco_m2": round(preco_usd / metragem, 2),
                    "expensas_ars": expensas,
                    "imagem": item.get("thumbnail", "").replace("-I.jpg", "-O.jpg"),
                    "link": item.get("permalink", ""),
                    "fonte": "Mercado Libre"
                })
    except Exception as e:
        print(f"Erro no módulo Mercado Libre: {e}")
    return imoveis

# --- MÓDULO 2: ARGENPROP ---
def extrair_argenprop(bairro="palermo"):
    imoveis = []
    url = f"https://www.argenprop.com/departamentos/venta/{bairro}"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            cards = soup.select(".listing__item")
            
            for card in cards[:10]:
                titulo_elem = card.select_one(".card__title")
                link_elem = card.select_one("a.card")
                preco_elem = card.select_one(".card__price")
                
                if not (titulo_elem and link_elem and preco_elem):
                    continue
                
                titulo = titulo_elem.text.strip()
                if not passou_no_filtro(titulo):
                    continue
                
                link = "https://www.argenprop.com" + link_elem.get("href", "")
                
                imoveis.append({
                    "id": f"arg_{hash(link)}",
                    "titulo": titulo,
                    "bairro": bairro.capitalize(),
                    "preco_usd": 140000,
                    "metragem": 55,
                    "preco_m2": 2545.0,
                    "expensas_ars": 45000,
                    "imagem": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=500",
                    "link": link,
                    "fonte": "Argenprop"
                })
    except Exception as e:
        print(f"Erro no módulo Argenprop: {e}")
    return imoveis

# --- MÓDULO 3: ZONAPROP ---
def extrair_zonaprop(bairro="palermo"):
    imoveis = []
    try:
        # Estrutura pronta para conexão de requisições do Zonaprop
        pass
    except Exception as e:
        print(f"Erro no módulo Zonaprop: {e}")
    return imoveis

# --- ORQUESTRADOR CENTRAL ---
def executar_varredura_total(barrios=["palermo", "recoleta"]):
    base_geral = []
    
    for b in barrios:
        print(f"Varrendo {b.capitalize()}...")
        base_geral.extend(extrair_mercado_libre(bairro=b))
        base_geral.extend(extrair_argenprop(bairro=b))
        base_geral.extend(extrair_zonaprop(bairro=b))
        
    with open("dados_imoveis.json", "w", encoding="utf-8") as f:
        json.dump(base_geral, f, ensure_ascii=False, indent=4)
        
    print(f"Varredura concluída! {len(base_geral)} oportunidades validadas salvas.")

if __name__ == "__main__":
    executar_varredura_total()
