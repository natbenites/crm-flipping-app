import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time

# Puxa a chave gratuita escondida no GitHub
API_KEY = os.environ.get("SCRAPER_API_KEY")

TERMOS_EXCLUSAO = [
    "sin ascensor", "acceso por escalera", "primer piso por escalera",
    "no acepta mascotas", "sin mascotas", "alquiler temporal",
    "ocupado", "sin escritura", "cesion de derechos", "indiviso",
    "solo efectivo", "lateral ciego", "sin luz", "interno ciego"
]

def passou_no_filtro(texto):
    if not texto: return True
    return not any(termo in texto.lower() for termo in TERMOS_EXCLUSAO)

def acessar_com_proxy(url):
    """Bypassa o Cloudflare usando a cota gratuita do ScraperAPI"""
    if API_KEY:
        payload = {'api_key': API_KEY, 'url': url}
        return requests.get('http://api.scraperapi.com', params=payload, timeout=30)
    return requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)

# --- MERCADO LIBRE (API Oficial, não consome cota do Proxy) ---
def extrair_mercado_libre(bairro="palermo"):
    imoveis = []
    url = f"https://api.mercadolibre.com/sites/MLA/search?category=MLA1459&q={bairro}%20buenos%20aires&limit=20"
    try:
        res = requests.get(url, timeout=15)
        for item in res.json().get("results", []):
            if item.get("currency_id") != "USD": continue
            titulo = item.get("title", "")
            if not passou_no_filtro(titulo): continue

            metragem = next((a.get("value_struct", {}).get("number", 0) for a in item.get("attributes", []) if a.get("id") == "TOTAL_AREA"), 0)
            if metragem <= 0: continue

            preco = item.get("price", 0)
            imoveis.append({
                "id": f"ml_{item.get('id')}",
                "titulo": titulo,
                "bairro": bairro.capitalize(),
                "preco_usd": preco,
                "metragem": metragem,
                "preco_m2": round(preco / metragem, 2),
                "link": item.get("permalink", ""),
                "fonte": "Mercado Libre"
            })
    except Exception as e:
        print(f"Erro Mercado Libre ({bairro}): {e}")
    return imoveis

# --- ARGENPROP ---
def extrair_argenprop(bairro="palermo"):
    imoveis = []
    url = f"https://www.argenprop.com/departamentos/venta/{bairro}"
    try:
        res = acessar_com_proxy(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            for card in soup.select(".listing__item")[:15]:
                titulo_elem = card.select_one(".card__title")
                preco_elem = card.select_one(".card__price")
                link_elem = card.select_one("a.card")
                
                if not (titulo_elem and preco_elem and link_elem): continue
                if not passou_no_filtro(titulo_elem.text): continue
                if "USD" not in preco_elem.text: continue
                
                preco = int(re.sub(r"[^\d]", "", preco_elem.text))
                metragem = 0
                for det in card.select(".card__common-data .main-features li"):
                    if "m²" in det.text.lower():
                        nums = re.sub(r"[^\d]", "", det.text)
                        if nums: metragem = int(nums)

                if preco > 0 and metragem > 0:
                    imoveis.append({
                        "id": f"arg_{hash(link_elem.get('href'))}",
                        "titulo": titulo_elem.text.strip(),
                        "bairro": bairro.capitalize(),
                        "preco_usd": preco,
                        "metragem": metragem,
                        "preco_m2": round(preco / metragem, 2),
                        "link": "https://www.argenprop.com" + link_elem.get("href"),
                        "fonte": "Argenprop"
                    })
    except Exception as e:
        print(f"Erro Argenprop ({bairro}): {e}")
    return imoveis

# --- ZONAPROP ---
def extrair_zonaprop(bairro="palermo"):
    imoveis = []
    url = f"https://www.zonaprop.com.ar/departamentos-venta-{bairro}.html"
    try:
        res = acessar_com_proxy(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            for card in soup.select("div[data-qa='posting-card']")[:15]:
                preco_elem = card.select_one("div[data-qa='POSTING_CARD_PRICE']")
                if not preco_elem or "USD" not in preco_elem.text: continue
                
                preco = int(re.sub(r"[^\d]", "", preco_elem.text))
                metragem = 0
                for feat in card.select("span[data-qa='POSTING_CARD_FEATURES']"):
                    if "m²" in feat.text.lower():
                        nums = re.sub(r"[^\d]", "", feat.text)
                        if nums: metragem = int(nums)

                link_attr = card.get("data-to-posting")
                if preco > 0 and metragem > 0 and link_attr:
                    imoveis.append({
                        "id": f"zp_{hash(link_attr)}",
                        "titulo": "Imóvel Zonaprop", 
                        "bairro": bairro.capitalize(),
                        "preco_usd": preco,
                        "metragem": metragem,
                        "preco_m2": round(preco / metragem, 2),
                        "link": f"https://www.zonaprop.com.ar{link_attr}",
                        "fonte": "Zonaprop"
                    })
    except Exception as e:
        print(f"Erro Zonaprop ({bairro}): {e}")
    return imoveis

def executar_varredura():
    bairros = ["palermo", "recoleta"]
    base_geral = []
    
    for b in bairros:
        print(f"Processando {b.capitalize()}...")
        base_geral.extend(extrair_mercado_libre(b))
        base_geral.extend(extrair_argenprop(b))
        base_geral.extend(extrair_zonaprop(b))
        time.sleep(1) # Intervalo seguro

    if base_geral:
        base_unica = {item['link']: item for item in base_geral}.values()
        with open("dados_imoveis.json", "w", encoding="utf-8") as f:
            json.dump(list(base_unica), f, ensure_ascii=False, indent=4)
        print(f"Sucesso! {len(base_unica)} imóveis reais capturados e salvos.")

if __name__ == "__main__":
    executar_varredura()
