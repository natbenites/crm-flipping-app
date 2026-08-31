import requests
from bs4 import BeautifulSoup
import json
import re
import time

# Trava anticiladas: imóveis com estes termos são descartados automaticamente
TERMOS_EXCLUSAO = [
    "sin ascensor", "acceso por escalera", "primer piso por escalera",
    "no acepta mascotas", "sin mascotas", "alquiler temporal",
    "ocupado", "sin escritura", "cesion de derechos", "indiviso",
    "solo efectivo", "lateral ciego", "sin luz", "interno ciego"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7",
    "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1"
}

def passou_no_filtro(texto):
    """Retorna False se encontrar qualquer termo anticilada no título/descrição."""
    if not texto:
        return True
    texto_lc = texto.lower()
    return not any(termo in texto_lc for termo in TERMOS_EXCLUSAO)

# --- MÓDULO 1: MERCADO LIBRE ---
def extrair_mercado_libre(bairro="palermo", limite=50):
    imoveis = []
    url = f"https://api.mercadolibre.com/sites/MLA/search?category=MLA1459&q={bairro}%20buenos%20aires&limit={limite}"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=12)
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
        print(f"Erro no Mercado Libre ({bairro}): {e}")
    return imoveis

# --- MÓDULO 2: ARGENPROP ---
def extrair_argenprop(bairro="palermo", paginas=2):
    imoveis = []
    for pag in range(1, paginas + 1):
        url = f"https://www.argenprop.com/departamentos/venta/{bairro}-pagina-{pag}" if pag > 1 else f"https://www.argenprop.com/departamentos/venta/{bairro}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=12)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                cards = soup.select(".listing__item")
                
                for card in cards:
                    titulo_elem = card.select_one(".card__title")
                    link_elem = card.select_one("a.card")
                    preco_elem = card.select_one(".card__price")
                    img_elem = card.select_one(".card__photos img")
                    
                    if not (titulo_elem and link_elem and preco_elem):
                        continue
                    
                    titulo = titulo_elem.text.strip()
                    if not passou_no_filtro(titulo):
                        continue
                    
                    texto_preco = preco_elem.text.strip()
                    if "USD" not in texto_preco:
                        continue
                    
                    preco_numeros = re.sub(r"[^\d]", "", texto_preco)
                    preco_usd = int(preco_numeros) if preco_numeros else 0
                    
                    detalhes = card.select(".card__common-data .main-features li")
                    metragem = 0
                    for det in detalhes:
                        texto_det = det.text.strip().lower()
                        if "m²" in texto_det or "cubiertos" in texto_det:
                            m_num = re.sub(r"[^\d]", "", texto_det)
                            if m_num:
                                metragem = int(m_num)
                                break
                    
                    if preco_usd == 0 or metragem == 0:
                        continue
                    
                    link = "https://www.argenprop.com" + link_elem.get("href", "")
                    imagem = img_elem.get("data-src") or img_elem.get("src") if img_elem else "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=500"
                    
                    imoveis.append({
                        "id": f"arg_{hash(link)}",
                        "titulo": titulo,
                        "bairro": bairro.capitalize(),
                        "preco_usd": preco_usd,
                        "metragem": metragem,
                        "preco_m2": round(preco_usd / metragem, 2),
                        "expensas_ars": 0,
                        "imagem": imagem,
                        "link": link,
                        "fonte": "Argenprop"
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Erro no Argenprop ({bairro}): {e}")
    return imoveis

# --- MÓDULO 3: ZONAPROP ---
def extrair_zonaprop(bairro="palermo", paginas=1):
    imoveis = []
    # Mapeamento simples de slugs do Zonaprop
    bairro_slug = bairro.lower().replace(" ", "-")
    
    for pag in range(1, paginas + 1):
        url = f"https://www.zonaprop.com.ar/departamentos-venta-{bairro_slug}-pagina-{pag}.html" if pag > 1 else f"https://www.zonaprop.com.ar/departamentos-venta-{bairro_slug}.html"
        
        try:
            res = requests.get(url, headers=HEADERS, timeout=12)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                cards = soup.select("div[data-qa='posting-card']")
                
                for card in cards:
                    # Título / Endereço
                    loc_elem = card.select_one("div[data-qa='POSTING_CARD_LOCATION']")
                    title_elem = card.select_one(".postingCardTitle") or loc_elem
                    
                    # Link
                    link_attr = card.get("data-to-posting")
                    link = f"https://www.zonaprop.com.ar{link_attr}" if link_attr else ""
                    
                    # Preço
                    price_elem = card.select_one("div[data-qa='POSTING_CARD_PRICE']")
                    
                    # Foto
                    img_elem = card.select_one("img")
                    
                    if not (title_elem and price_elem and link):
                        continue
                    
                    titulo = title_elem.text.strip()
                    if not passou_no_filtro(titulo):
                        continue
                        
                    texto_preco = price_elem.text.strip()
                    if "USD" not in texto_preco and "U$S" not in texto_preco:
                        continue
                    
                    preco_numeros = re.sub(r"[^\d]", "", texto_preco)
                    preco_usd = int(preco_numeros) if preco_numeros else 0
                    
                    # Metragem
                    features = card.select("span[data-qa='POSTING_CARD_FEATURES']")
                    metragem = 0
                    for feat in features:
                        text_feat = feat.text.strip().lower()
                        if "m²" in text_feat:
                            m_num = re.sub(r"[^\d]", "", text_feat)
                            if m_num:
                                metragem = int(m_num)
                                break
                    
                    if preco_usd == 0 or metragem == 0:
                        continue
                        
                    imagem = img_elem.get("src") if img_elem else "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=500"
                    
                    imoveis.append({
                        "id": f"zona_{hash(link)}",
                        "titulo": titulo,
                        "bairro": bairro.capitalize(),
                        "preco_usd": preco_usd,
                        "metragem": metragem,
                        "preco_m2": round(preco_usd / metragem, 2),
                        "expensas_ars": 0,
                        "imagem": imagem,
                        "link": link,
                        "fonte": "Zonaprop"
                    })
            else:
                print(f"Zonaprop retornou código HTTP {res.status_code} para {bairro}.")
            time.sleep(1.5)
        except Exception as e:
            print(f"Erro no Zonaprop ({bairro}): {e}")
            
    return imoveis

# --- ORQUESTRADOR CENTRAL ---
def executar_varredura_total():
    barrios = ["palermo", "recoleta", "belgrano", "caballito", "barrio norte"]
    base_geral = []
    
    for b in barrios:
        print(f"Varrendo mercado em {b.capitalize()}...")
        base_geral.extend(extrair_mercado_libre(bairro=b, limite=50))
        base_geral.extend(extrair_argenprop(bairro=b, paginas=2))
        base_geral.extend(extrair_zonaprop(bairro=b, paginas=1))
        
    print(f"Total capturado (bruto): {len(base_geral)}")
    
    # Remoção de duplicatas por link
    base_unica = {item['link']: item for item in base_geral}.values()
    lista_final = list(base_unica)

    with open("dados_imoveis.json", "w", encoding="utf-8") as f:
        json.dump(lista_final, f, ensure_ascii=False, indent=4)
        
    print(f"Varredura concluída! {len(lista_final)} imóveis processados e salvos.")

if __name__ == "__main__":
    executar_varredura_total()
