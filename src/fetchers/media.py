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
        # DolarHoy no tiene sección estricta de cripto noticias, buscaremos en su portada 
        # o sección noticias la palabra cripto/bitcoin si es posible. Por simplicidad sacaremos 
        # la primera noticia principal si no encontramos algo especifico
        url = "https://dolarhoy.com/"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Extraer primer título (ajustar clase según inspección)
            articulo = soup.find('a', class_='title')
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
            articulo = soup.find('h2')
            if articulo and articulo.parent and articulo.parent.name == 'a':
                titulo = articulo.text.strip()
                link = "https://www.infobae.com" + articulo.parent['href'] if not articulo.parent['href'].startswith('http') else articulo.parent['href']
                resultados.append(f"📰 **Infobae:** [{titulo}]({link})")
            elif articulo and articulo.find('a'):
                titulo = articulo.find('a').text.strip()
                link = "https://www.infobae.com" + articulo.find('a')['href'] if not articulo.find('a')['href'].startswith('http') else articulo.find('a')['href']
                resultados.append(f"📰 **Infobae:** [{titulo}]({link})")
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
