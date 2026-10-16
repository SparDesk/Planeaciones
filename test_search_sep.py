import re
import urllib3
import requests
from bs4 import BeautifulSoup
from typing import Tuple

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def buscar_programa_sintetico_sep(fase_seleccionada: str, max_resultados: int = 3) -> Tuple[str, bool]:
    """
    Búsqueda auxiliar de respaldo para el Programa Sintético oficial de la SEP.
    Utiliza googlesearch-python y requests/BeautifulSoup con el término:
    site:sep.gob.mx OR site:conaliteg.sep.gob.mx "Programa Sintético" "Fase {fase_seleccionada}"
    """
    # Normalizar Fase (ej. "5" o "Fase 5")
    fase_limpia = str(fase_seleccionada).replace("Fase", "").strip()
    fase_termino = f"Fase {fase_limpia}" if fase_limpia else "Fase 5"

    query = f'site:sep.gob.mx OR site:conaliteg.sep.gob.mx "Programa Sintético" "{fase_termino}"'
    urls = []

    # 1. Intentar con googlesearch-python
    try:
        from googlesearch import search
        for url in search(query, num_results=max_resultados, lang="es", timeout=5):
            u = getattr(url, "url", url) if not isinstance(url, str) else url
            if u and isinstance(u, str) and u.startswith("http"):
                urls.append(u)
            if len(urls) >= max_resultados:
                break
    except Exception as e:
        print(f"Nota en googlesearch: {e}")

    # 2. Respaldo adicional si Google bloqueó o retornó 0 enlaces
    if not urls:
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                ddg_res = list(ddgs.text(query, max_results=max_resultados))
                for item in ddg_res:
                    href = item.get("href") or item.get("link")
                    if href and ("sep.gob.mx" in href or "conaliteg.sep.gob.mx" in href):
                        urls.append(href)
        except Exception as e:
            print(f"Nota en búsqueda secundaria: {e}")

    # 3. Extraer contenido de las URLs encontradas usando requests y BeautifulSoup
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-MX,es;q=0.9"
    }

    resumenes = []
    for u in urls[:max_resultados]:
        try:
            resp = requests.get(u, headers=headers, timeout=5, verify=False)
            if resp.status_code == 200 and resp.text:
                soup = BeautifulSoup(resp.text, "html.parser")
                for s in soup(["script", "style", "nav", "footer", "header", "noscript"]):
                    s.decompose()
                parrafos = [
                    p.get_text(strip=True)
                    for p in soup.find_all(["p", "h1", "h2", "h3", "li"])
                    if len(p.get_text(strip=True)) > 30
                ]
                texto_pagina = " ".join(parrafos[:15])
                if len(texto_pagina.strip()) > 80:
                    resumenes.append(f"Fuente ({u}):\n{texto_pagina[:1200]}")
        except Exception:
            continue

    if resumenes:
        resumen_final = "\n\n---\n\n".join(resumenes)
        return resumen_final, True

    return "", False

if __name__ == "__main__":
    res, ok = buscar_programa_sintetico_sep("Fase 5")
    print("Scraping exitoso:", ok)
    print("Longitud resumen:", len(res))
    if not ok:
        semana = 20
        fase = "Fase 5".replace("Fase", "").strip()
        fallback = f"Como no se proporcionó un documento oficial, utiliza tu conocimiento interno y capacidad de búsqueda para acceder a los lineamientos de la Nueva Escuela Mexicana (SEP) para la Fase {fase} y Semana {semana}."
        print("Fallback prompt:", fallback)
