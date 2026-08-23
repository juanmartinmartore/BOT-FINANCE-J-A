import feedparser
import requests
from bs4 import BeautifulSoup
import json
import os

class HistoryManager:
    def __init__(self, filepath="data/sent_news.json", max_history=100):
        self.filepath = filepath
        self.max_history = max_history
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _save_history(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.history, f)

    def is_seen(self, url):
        return url in self.history

    def mark_seen(self, url):
        if url not in self.history:
            self.history.append(url)
            # Mantener el historial dentro de un límite para que no crezca infinitamente
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]
            self._save_history()

def get_latest_news(history_manager=None):
    """Obtiene la última noticia inédita de medios seleccionados combinando RSS y Scraping."""
    resultados = []
    headers = {"User-Agent": "Mozilla/5.0"}
    
    def process_article(source_name, entries, get_title_link):
        for entry in entries:
            try:
                titulo, link = get_title_link(entry)
                if not titulo or not link: continue
                
                # Deduplicación
                if history_manager and history_manager.is_seen(link):
                    continue
                
                resultados.append(f"📰 **{source_name}:** [{titulo}]({link})")
                if history_manager:
                    history_manager.mark_seen(link)
                return True
            except Exception as e:
                pass
        return False

    # 1. Forbes IA & Big Data
    try:
        url = "https://www.forbesargentina.com/temas/ia-big-data-t54"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            articulos = soup.find_all('h2')
            
            def extract_forbes(h2):
                a_tag = h2.find('a')
                if not a_tag: return None, None
                link = "https://www.forbesargentina.com" + a_tag['href'] if not a_tag['href'].startswith('http') else a_tag['href']
                return a_tag.text.strip(), link
                
            process_article("Forbes IA & Big Data", articulos, extract_forbes)
    except Exception as e:
        print(f"Error Forbes IA: {e}")

    # 2. Forbes Finanzas
    try:
        url = "https://www.forbesargentina.com/temas/finanzas-t17"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            articulos = soup.find_all('h2')
            
            def extract_forbes(h2):
                a_tag = h2.find('a')
                if not a_tag: return None, None
                link = "https://www.forbesargentina.com" + a_tag['href'] if not a_tag['href'].startswith('http') else a_tag['href']
                return a_tag.text.strip(), link
                
            process_article("Forbes Finanzas", articulos, extract_forbes)
    except Exception as e:
        print(f"Error Forbes Finanzas: {e}")

    # 3. DolarHoy
    try:
        url = "https://dolarhoy.com/"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Buscamos SOLO links que vayan a /noticias/ para evitar publicidades engañosas (ej. Bull Market)
            articulos = [a for a in soup.find_all('a', href=True) if '/noticias/' in a['href'] and len(a.text.strip()) > 10]
            
            def extract_dh(a_tag):
                titulo = a_tag.text.strip()
                link = "https://dolarhoy.com" + a_tag['href'] if not a_tag['href'].startswith('http') else a_tag['href']
                return titulo, link
                
            process_article("DólarHoy", articulos, extract_dh)
    except Exception as e:
        print(f"Error DolarHoy: {e}")

    # 4. Infobae Economía
    try:
        url = "https://www.infobae.com/economia/"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Buscamos a_tags con h2 adentro para extraer solo el título principal y evitar el autor/bajada
            articulos = soup.find_all('a', href=True)
            
            def extract_infobae(a_tag):
                h2 = a_tag.find('h2')
                if not h2: return None, None
                titulo = h2.text.strip()
                if len(titulo) < 15: return None, None
                link = "https://www.infobae.com" + a_tag['href'] if not a_tag['href'].startswith('http') else a_tag['href']
                return titulo, link
                
            process_article("Infobae", articulos, extract_infobae)
    except Exception as e:
        print(f"Error Infobae: {e}")

    # 5. Ámbito Economía
    try:
        feed = feedparser.parse("https://www.ambito.com/rss/economia.xml")
        
        def extract_rss(entry):
            return entry.title, entry.link
            
        process_article("Ámbito", feed.entries, extract_rss)
    except Exception as e:
        print(f"Error Ámbito RSS: {e}")
            
    return resultados

def get_latest_videos(history_manager=None):
    """Obtiene los últimos videos de canales de YouTube clave vía RSS, filtrando Shorts."""
    canales_yt = {
        "Joven Inversor": "UCnOWLhk15P-gUV7RdehAI2Q",
        "Lubruuu": "UC76wQE_p3uZ5gDUQILhwIlg",
        "Bull Market": "UCXgsCoIhEUIwWvGK_JDY21w",
        "Inverarg": "UCzjPGrukIV5DDkLDQTKgmgA"
    }
    
    resultados = []
    
    for creador, channel_id in canales_yt.items():
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                titulo = entry.title
                link = entry.link
                
                # Heurísticas rápidas para detectar Shorts: 
                # 1. El título dice #shorts o #Shorts
                if "#shorts" in titulo.lower() or "short" in titulo.lower():
                    continue
                    
                # 2. Verificación por HTTP (La más precisa). Extraemos el ID del video y consultamos a YouTube
                video_id = link.split("v=")[-1]
                try:
                    # Pedimos el enlace del short permitiendo redirect. Si Youtube redirige al watch, NO es un short.
                    r_check = requests.head(f"https://www.youtube.com/shorts/{video_id}", allow_redirects=True, timeout=5)
                    if "/shorts/" in r_check.url:
                        # La URL final sigue siendo /shorts/, entonces ES un short, lo saltamos
                        continue
                except:
                    pass
                
                if history_manager and history_manager.is_seen(link):
                    continue
                    
                resultados.append(f"🎥 **{creador}:** [{titulo}]({link})")
                if history_manager:
                    history_manager.mark_seen(link)
                break # Agarramos solo 1 video largo inédito por canal
        except Exception as e:
            print(f"Error procesando YouTube de {creador}: {e}")
            
    return resultados
