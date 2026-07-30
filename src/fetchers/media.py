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
            # Extraer cualquier enlace con clase title o dentro de h4/h3
            articulo = soup.find('a', class_='title')
            if not articulo:
                # Fallback: buscar el primer enlace largo en un h4 o titular principal
                h4 = soup.find('h4')
                if h4 and h4.find('a'):
                    articulo = h4.find('a')
            if articulo:
                titulo = articulo.text.strip()
                link = "https://dolarhoy.com" + articulo['href'] if not articulo['href'].startswith('http') else articulo['href']
                resultados.append(f"📰 **DólarHoy:** [{titulo}]({link})")
    except Exception as e:
        print(f"Error DolarHoy: {e}")

    # 4. Infobae Economía (Scraping)
    try:
        url = "https://www.infobae.com/economia/"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Las notas principales suelen estar en a.story-card-info-title o similar, buscamos h2
            titulos = soup.find_all(['h2', 'h1'])
            for h in titulos:
                a_tag = h.find('a')
                if a_tag and a_tag.get('href'):
                    titulo = a_tag.text.strip()
                    if len(titulo) > 20: # Evitar links vacíos o de menú
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
