import feedparser

def get_latest_news():
    """Obtiene la última noticia de fuentes RSS seleccionadas."""
    
    fuentes_diarios = {
        "Infobae": "https://www.infobae.com/feed/economia/",
        "Ámbito": "https://www.ambito.com/rss/economia.xml",
        "El Cronista": "https://www.cronista.com/files/rss/finanzasmercados.xml"
    }
    
    resultados = []
    
    for medio, url in fuentes_diarios.items():
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                # Tomamos solo la primera noticia (la más reciente)
                entry = feed.entries[0]
                titulo = entry.title
                link = entry.link
                resultados.append(f"📰 **{medio}:** [{titulo}]({link})")
        except Exception as e:
            print(f"Error procesando RSS de {medio}: {e}")
            
    return resultados

def get_latest_videos():
    """Obtiene los últimos videos de canales de YouTube clave vía RSS."""
    
    # IDs de canales extraídos a modo de ejemplo (se pueden ajustar)
    canales_yt = {
        "Joven Inversor": "UCNt68gM7z5R2zL-Uf9k5Pqw",
        "Cripto Norber": "UC2X4pLpQk8z5l5b0hE9VzLw", # IDs aproximados/placeholder
        "Inverarg": "UCT6K6Y4y7h2J4t7n4s_1_zA" 
    }
    
    resultados = []
    
    for creador, channel_id in canales_yt.items():
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                entry = feed.entries[0]
                titulo = entry.title
                link = entry.link
                resultados.append(f"🎥 **{creador}:** [{titulo}]({link})")
        except Exception as e:
            print(f"Error procesando YouTube de {creador}: {e}")
            
    return resultados
