import feedparser
import requests
from bs4 import BeautifulSoup

def get_latest_news():
    """Obtiene la última noticia de medios seleccionados combinando RSS y Scraping."""
    resultados = []
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # 1. Forbes IA & Big Data (Scraping)
    try:
        url = "https://www.forbesargentina.com/temas/ia-big-data-t54"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Las noticias en Forbes suelen tener links dentro de h2 o div con clases de título
            articulo = soup.find('h2')
            if articulo and articulo.find('a'):
                a_tag = articulo.find('a')
                titulo = a_tag.text.strip()
                link = a_tag['href']
                if not link.startswith('http'):
                    link = "https://www.forbesargentina.com" + link
                resultados.append(f"📰 **Forbes IA & Big Data:** [{titulo}]({link})")
    except Exception as e:
        print(f"Error Forbes IA: {e}")

    # 2. Forbes Finanzas (Scraping)
    try:
        url = "https://www.forbesargentina.com/temas/finanzas-t17"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            articulo = soup.find('h2')
            if articulo and articulo.find('a'):
                a_tag = articulo.find('a')
                titulo = a_tag.text.strip()
                link = a_tag['href']
                if not link.startswith('http'):
                    link = "https://www.forbesargentina.com" + link
                resultados.append(f"📰 **Forbes Finanzas:** [{titulo}]({link})")
    except Exception as e:
        print(f"Error Forbes Finanzas: {e}")

# 3. DolarHoy Cripto (Scraping)
    try:
        url = "https://dolarhoy.com/"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # DolarHoy suele poner las noticias en bloques con clase 'topic' o directamente en hipervínculos dentro de 'div'
            noticia_encontrada = False
            for enlace in soup.find_all('a', href=True):
                # Buscamos un enlace que parezca una noticia (más de 20 caracteres y sin estar en el header)
                if '/noticias/' in enlace['href'] or len(enlace.text.strip()) > 30:
                    titulo = enlace.text.strip()
                    link = "https://dolarhoy.com" + enlace['href'] if not enlace['href'].startswith('http') else enlace['href']
                    resultados.append(f"📰 **DólarHoy:** [{titulo}]({link})")
                    noticia_encontrada = True
                    break
    except Exception as e:
        print(f"Error DolarHoy: {e}")

    # 4. Infobae Economía (Scraping)
    try:
        url = "https://www.infobae.com/economia/"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Infobae cambió sus clases dinámicas. Buscamos el primer link dentro de la estructura principal de la nota
            titulos = soup.find_all(['h2', 'a'])
            for elemento in titulos:
                if elemento.name == 'a' and elemento.get('href') and len(elemento.text.strip()) > 35:
                    titulo = elemento.text.strip()
                    link = "https://www.infobae.com" + elemento['href'] if not elemento['href'].startswith('http') else elemento['href']
                    resultados.append(f"📰 **Infobae:** [{titulo}]({link})")
                    break
                elif elemento.name == 'h2':
                    a_tag = elemento.find('a')
                    if a_tag and a_tag.get('href') and len(a_tag.text.strip()) > 35:
                        titulo = a_tag.text.strip()
                        link = "https://www.infobae.com" + a_tag['href'] if not a_tag['href'].startswith('http') else a_tag['href']
                        resultados.append(f"📰 **Infobae:** [{titulo}]({link})")
                        break
    except Exception as e:
        print(f"Error Infobae: {e}")

    # 5. Ámbito Economía (RSS)
    try:
        url = "https://www.ambito.com/rss/economia.xml"
        feed = feedparser.parse(url)
        if feed.entries:
            entry = feed.entries[0]
            resultados.append(f"📰 **Ámbito:** [{entry.title}]({entry.link})")
    except Exception as e:
        print(f"Error Ámbito RSS: {e}")
            
    return resultados

def get_latest_videos():
    """Obtiene los últimos videos de canales de YouTube clave vía RSS."""
    canales_yt = {
        "Joven Inversor": "UCjLw8VmwHxDdmqChMFwyWw",
        "Cripto Norber": "UCNa-pOxhhp3hWfAGuTnWhCg"
    }
    resultados = []
    for creador, channel_id in canales_yt.items():
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                entry = feed.entries[0]
                resultados.append(f"🎥 **{creador}:** [{entry.title}]({entry.link})")
        except Exception as e:
            print(f"Error procesando YouTube de {creador}: {e}")
    return resultados
