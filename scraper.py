import requests
import json
import os

# Puxa a chave gratuita que você já configurou no GitHub
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

def extrair_mercado_libre(bairro="palermo", limite=50):
    imoveis = []
    url = f"https://api.mercadolibre.com/sites/MLA/search?category=MLA1459&q={bairro}%20buenos%20aires&limit={limite}"
    
    try:
        # AQUI ESTÁ A SOLUÇÃO DEFINITIVA: O Mercado Libre agora usa o disfarce (ScraperAPI)
        url_busca = f"http://api.scraperapi.com?api_key={API_KEY}&url={url}" if API_KEY else url
        res = requests.get(url_busca, timeout=25)
        
        if res.status_code == 200:
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
        else:
            print(f"Erro Mercado Libre ({bairro}): Status {res.status_code}")
    except Exception as e:
        print(f"Exceção Mercado Libre ({bairro}): {e}")
        
    return imoveis

def executar_varredura():
    bairros = ["palermo", "recoleta", "belgrano", "caballito", "barrio norte"]
    base_geral = []
    
    for b in bairros:
        print(f"Buscando ofertas com proxy em {b.capitalize()}...")
        base_geral.extend(extrair_mercado_libre(b, limite=50))

    if base_geral:
        base_unica = {item['link']: item for item in base_geral}.values()
        with open("dados_imoveis.json", "w", encoding="utf-8") as f:
            json.dump(list(base_unica), f, ensure_ascii=False, indent=4)
        print(f"Sucesso! {len(base_unica)} imóveis capturados com a ScraperAPI.")
    else:
        raise Exception("Nenhum imóvel foi capturado. O robô foi interrompido.")

if __name__ == "__main__":
    executar_varredura()
