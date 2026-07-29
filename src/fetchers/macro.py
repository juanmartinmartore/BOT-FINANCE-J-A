import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_dolares():
    """Obtiene Dólar Blue, Oficial y CCL desde DolarAPI."""
    dolares = {}
    try:
        urls = {
            "Blue": "https://dolarapi.com/v1/dolares/blue",
            "Oficial": "https://dolarapi.com/v1/dolares/oficial",
            "CCL": "https://dolarapi.com/v1/dolares/contadoconliqui"
        }
        for nombre, url in urls.items():
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                dolares[nombre] = {
                    "compra": data.get("compra", 0),
                    "venta": data.get("venta", 0)
                }
    except Exception as e:
        print(f"Error fetching dolares: {e}")
    return dolares

def get_dolar_futuro():
    """Obtiene el próximo vencimiento de Dólar Futuro scrapeando Rofex o Ámbito."""
    try:
        url = "https://mercados.ambito.com/dolarfuturo/mercado"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) > 1:
                contrato = data[1]
                mes = contrato[0]
                valor = contrato[1]
                return f"{mes}: ${valor}"
    except Exception as e:
        print(f"Error fetching dolar futuro: {e}")
    return "No disponible"

def get_inflacion():
    """Obtiene el último dato de inflación desde una fuente pública."""
    try:
        url = "https://api.bcra.gob.ar/estadisticas/v1/principalesvariables"
        resp = requests.get(url, verify=False, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            resultados = data.get("results", [])
            for res in resultados:
                if res.get("idVariable") == 27:
                    fecha = res.get("fecha", "")[:7]
                    valor = res.get("valor", 0)
                    return f"{valor}% ({fecha})"
    except Exception as e:
        print(f"Error fetching inflacion: {e}")
    return "Dato demorado"
