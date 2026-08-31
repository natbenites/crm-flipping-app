import requests
from bs4 import BeautifulSoup
import json
import re
import os

API_KEY = os.environ.get("SCRAPER_API_KEY")

# Seu filtro anticiladas
TERMOS_EXCLUSAO = [
    "sin ascensor", "acceso por escalera", "primer piso por escalera",
    "no acepta mascotas", "sin mascotas", "alquiler temporal",
    "ocupado", "sin escritura", "cesion de derechos", "indiviso",
    "solo efectivo", "lateral ciego", "sin luz", "interno ciego"
]

def passou_no_filtro(texto):
    if not texto: return True
    return not any(termo in texto.lower() for termo in TERMOS_EXCLUSAO)

def extrair_mercado_libre(bairro="palermo"):
    imoveis = []
    url = f"https://api.mercadolibre.com/sites/MLA/search?category=MLA1459&q={bairro}%20buenos%20aires&limit=30"
    try:
        res = requests.get(url, timeout=10)
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
                "imagem": item.get("thumbnail", "").replace("-I.jpg", "-O.jpg"),
                "fonte": "Mercado Libre"
            })
    except:
        pass
    return imoveis

def extrair_argenprop(bairro="palermo"):
    imoveis = []
    url = f"https://www.argenprop.com/departamentos/venta/{bairro}"
    try:
        url_busca = f"http://api.scraperapi.com?api_key={API_KEY}&url={url}" if API_KEY else url
        res = requests.get(url_busca, timeout=30)
        soup = BeautifulSoup(res.text, "html.parser")
        
        for card in soup.select(".listing__item")[:20]:
            titulo_elem = card.select_one(".card__title")
            preco_elem = card.select_one(".card__price")
            link_elem = card.select_one("a.card")
            img_elem = card.select_one(".card__photos img")
            
            if not (titulo_elem and preco_elem and link_elem): continue
            if not passou_no_filtro(titulo_elem.text): continue
            if "USD" not in preco_elem.text: continue
            
            preco = int(re.sub(r"[^\d]", "", preco_elem.text))
            metragem = 0
            for det in card.select(".card__common-data .main-features li"):
                if "m²" in det.text.lower() or "cubiertos" in det.text.lower():
                    nums = re.sub(r"[^\d]", "", det.text)
                    if nums: metragem = int(nums)

            if preco > 0 and metragem > 0:
                imagem = img_elem.get("data-src") or img_elem.get("src") if img_elem else "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=500"
                imoveis.append({
                    "id": f"arg_{hash(link_elem.get('href'))}",
                    "titulo": titulo_elem.text.strip(),
                    "bairro": bairro.capitalize(),
                    "preco_usd": preco,
                    "metragem": metragem,
                    "preco_m2": round(preco / metragem, 2),
                    "link": "https://www.argenprop.com" + link_elem.get("href"),
                    "imagem": imagem,
                    "fonte": "Argenprop"
                })
    except:
        pass
    return imoveis

def extrair_remax(bairro="palermo"):
    imoveis = []
    url = f"https://www.remax.com.ar/pt-ar/imoveis/buenos-aires/{bairro.lower()}"
    try:
        url_busca = f"http://api.scraperapi.com?api_key={API_KEY}&url={url}" if API_KEY else url
        res = requests.get(url_busca, timeout=30)
        soup = BeautifulSoup(res.text, "html.parser")
        
        for card in soup.select(".property-card, .card-property")[:15]:
            titulo_elem = card.select_one(".title, .card-title, h2")
            preco_elem = card.select_one(".price, .price-value")
            link_elem = card.select_one("a")
            
            if not (titulo_elem and preco_elem and link_elem): continue
            titulo = titulo_elem.text.strip()
            if not passou_no_filtro(titulo): continue
            
            texto_preco = preco_elem.text.strip()
            if "USD" not in texto_preco and "U$S" not in texto_preco: continue
            preco = int(re.sub(r"[^\d]", "", texto_preco))
            
            metragem = 0
            m2_match = re.search(r"(\d+)\s*(m2|m²)", card.text.lower())
            if m2_match:
                metragem = int(m2_match.group(1))
                
            if preco > 0 and metragem > 0:
                link_parcial = link_elem.get("href", "")
                link_final = link_parcial if "remax.com.ar" in link_parcial else "https://www.remax.com.ar" + link_parcial
                
                imoveis.append({
                    "id": f"rmx_{hash(link_final)}",
                    "titulo": titulo,
                    "bairro": bairro.capitalize(),
                    "preco_usd": preco,
                    "metragem": metragem,
                    "preco_m2": round(preco / metragem, 2),
                    "link": link_final,
                    "imagem": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=500",
                    "fonte": "RE/MAX"
                })
    except:
        pass
    return imoveis

def executar_varredura():
    bairros = ["palermo", "recoleta", "belgrano"]
    base_geral = []
    
    for b in bairros:
        base_geral.extend(extrair_mercado_libre(b))
        base_geral.extend(extrair_argenprop(b))
        base_geral.extend(extrair_remax(b))

    if base_geral:
        base_unica = {item['link']: item for item in base_geral}.values()
        with open("dados_imoveis.json", "w", encoding="utf-8") as f:
            json.dump(list(base_unica), f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    executar_varredura()
