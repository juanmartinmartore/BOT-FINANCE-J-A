import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import lxml.html

def parse_price(val_str):
    """Limpia el string de precio y lo convierte a float.
       Ej: '$ 1380,00' -> 1380.00 / '$1380' -> 1380.0
    """
    cleaned = val_str.replace('$', '').replace('.', '').replace(',', '.').strip()
    return float(cleaned)

async def get_dollar_blue():
    url = "https://dolarhoy.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                html = await response.text()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None
            
    # Intentos de parseo
    try:
        # Intento 1: BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # En dolarhoy.com, el Dólar Blue suele tener un enlace a '/cotizaciondolarblue'
        link = soup.find('a', href=lambda h: h and 'dolar-blue' in h.lower() or 'dolarblue' in h.lower())
        
        if link:
            parent = link.find_parent('div', class_='tile')
            if not parent:
                parent = link.find_parent('div')
                
            compra_div = parent.find('div', class_='compra') if parent else None
            venta_div = parent.find('div', class_='venta') if parent else None
            
            if compra_div and venta_div:
                compra_val = compra_div.find('div', class_='val').text
                venta_val = venta_div.find('div', class_='val').text
                return {
                    "compra": parse_price(compra_val),
                    "venta": parse_price(venta_val),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
        # Intento 2: lxml y XPath (Fallback)
        tree = lxml.html.fromstring(html)
        # Buscar texto de enlace que contenga Dólar Blue o similar, o href con dolar-blue
        compra_node = tree.xpath('//a[contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "dolarblue") or contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "dolar-blue")]/ancestor::div[contains(@class, "tile")]//div[contains(@class, "compra")]//div[contains(@class, "val")]/text()')
        venta_node = tree.xpath('//a[contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "dolarblue") or contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "dolar-blue")]/ancestor::div[contains(@class, "tile")]//div[contains(@class, "venta")]//div[contains(@class, "val")]/text()')
        
        if compra_node and venta_node:
            compra_val = compra_node[0]
            venta_val = venta_node[0]
            return {
                "compra": parse_price(compra_val),
                "venta": parse_price(venta_val),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        
    return None
