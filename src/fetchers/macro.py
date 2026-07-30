import requests
import urllib3
from datetime import datetime, timezone, timedelta
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Zona horaria Argentina (UTC-3)
AR_TZ = timezone(timedelta(hours=-3))


def fmt_ar(valor, decimales=2):
    """Formatea un número al estilo argentino: 63378.5 → '63.378,50'."""
    try:
        numero = float(valor)
        formatted = f"{numero:,.{decimales}f}"
        # Swap: coma→X, punto→coma, X→punto
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return str(valor)


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
    """Obtiene los próximos vencimientos de Dólar Futuro desde Ámbito."""
    try:
        url = "https://mercados.ambito.com/dolarfuturo/datos"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) > 1:
                vencimientos = []
                # data[0] son los encabezados, tomamos hasta 12 filas de datos
                for contrato in data[1:13]:
                    if len(contrato) > 1:
                        mes = contrato[0]
                        valor = contrato[1]
                        vencimientos.append(f"{mes}: ${valor}")
                
                if vencimientos:
                    return " | ".join(vencimientos)
    except Exception as e:
        print(f"Error fetching dolar futuro: {e}")
    return "No disponible"


def get_bcra_variables():
    """Obtiene las principales variables del BCRA (réplica del #DATABCRA de Twitter)."""
    variables = {}
    try:
        url = "https://api.bcra.gob.ar/estadisticas/v1/principalesvariables"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, verify=False, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            resultados = data.get("results", [])

            # Mapa de IDs a nombres cortos (basado en la imagen de Twitter del BCRA)
            ids_deseados = {
                1: "Reservas Internacionales",
                4: "Tipo de Cambio Minorista",
                5: "BADLAR",
                6: "TM20",
            }

            for res in resultados:
                id_var = res.get("idVariable")
                if id_var in ids_deseados:
                    variables[ids_deseados[id_var]] = {
                        "valor": res.get("valor", 0),
                        "fecha": res.get("fecha", ""),
                        "descripcion": res.get("descripcion", "")
                    }
    except Exception as e:
        print(f"Error fetching BCRA variables: {e}")
    return variables


def get_inflacion():
    """Obtiene el último dato de inflación IPC publicado."""
    try:
        url = "https://apis.datos.gob.ar/series/api/series/"
        params = {
            "ids": "148.3_INIVELGENERAL_DICI_M_26",
            "last": "3", # Pedimos los últimos 3 meses por las dudas
            "format": "json"
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            datos = data.get("data", [])
            
            # Recorremos la lista al revés (desde el más reciente al más antiguo)
            for fila in reversed(datos):
                if len(fila) >= 2 and fila[1] is not None:
                    fecha_raw = fila[0]
                    valor = round(fila[1], 2)
                    
                    try:
                        fecha_dt = datetime.strptime(fecha_raw, "%Y-%m-%d")
                        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                                 "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
                        fecha_str = f"{meses[fecha_dt.month - 1]} {fecha_dt.year}"
                    except Exception:
                        fecha_str = fecha_raw
                        
                    return {"valor": valor, "fecha": fecha_str}
    except Exception as e:
        print(f"Error fetching inflacion (datos.gob.ar): {e}")

    # Intento 2: BCRA API - buscar cualquier variable con "inflación" en la descripción
    try:
        url = "https://api.bcra.gob.ar/estadisticas/v1/principalesvariables"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, verify=False, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            resultados = data.get("results", [])
            for res in resultados:
                desc = res.get("descripcion", "").lower()
                if "inflacion" in desc or "inflación" in desc or "ipc" in desc:
                    valor = res.get("valor", 0)
                    fecha = res.get("fecha", "")
                    return {"valor": valor, "fecha": fecha}
    except Exception as e:
        print(f"Error fetching inflacion (BCRA): {e}")

    return None
