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


def _parse_dolar_futuro_payload(data):
    """Normaliza diferentes formatos que devuelve Ámbito para el dólar futuro."""
    vencimientos = []
    
    # Nuevo formato: Ámbito ahora devuelve un dict donde las keys son '1', '3', '5'...
    if isinstance(data, dict) and '1' in data:
        # Ordenamos las keys numericamente para mantener el orden cronologico
        for key in sorted(data.keys(), key=lambda x: int(x) if x.isdigit() else 999):
            if key.isdigit():
                contrato_info = data[key]
                mes = contrato_info.get("contrato", "").replace("Dólar ", "").replace("Dolar ", "").replace("D\ufffdlar ", "")
                valor = contrato_info.get("venta")
                if not valor or valor == "-":
                    valor = contrato_info.get("compra")
                
                if mes and valor and valor != "-":
                    vencimientos.append(f"{mes}: ${valor}")
                    if len(vencimientos) >= 12:  # Limitar a los próximos 12 meses
                        break
                        
    # Formato viejo o lista genérica
    elif isinstance(data, list):
        rows = data[1:] if len(data) > 0 and isinstance(data[0], list) else data
        for contrato in rows[:12]:
            if isinstance(contrato, dict):
                mes = contrato.get("mes") or contrato.get("vencimiento") or contrato.get("title") or ""
                valor = contrato.get("valor") or contrato.get("price") or contrato.get("ultimo") or ""
            elif isinstance(contrato, (list, tuple)) and len(contrato) >= 2:
                mes = contrato[0]
                valor = contrato[1]
            else:
                continue
            if mes and valor:
                vencimientos.append(f"{mes}: ${valor}")

    return " | ".join(vencimientos) if vencimientos else None


def get_dolar_futuro():
    """Obtiene los próximos vencimientos de Dólar Futuro desde Ámbito."""
    try:
        url = "https://mercados.ambito.com/dolarfuturo/datos"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            resultado = _parse_dolar_futuro_payload(data)
            if resultado:
                return resultado
    except Exception as e:
        print(f"Error fetching dolar futuro: {e}")
    return "No disponible"


def get_bcra_variables():
    """
    Obtiene las principales variables del BCRA (réplica del #DATABCRA de Twitter).
    Actualmente desactivado porque las APIs del BCRA (v1 y v2) fueron deprecadas.
    Retorna un diccionario vacío para ocultar esta sección limpiamente en Discord.
    """
    return {}


def get_inflacion():
    """Obtiene el último dato de inflación IPC publicado."""
    try:
        url = "https://api.argentinadatos.com/v1/finanzas/indices/inflacion"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            if data and len(data) > 0:
                ultimo = data[-1]
                fecha_raw = ultimo.get("fecha", "")
                valor = round(ultimo.get("valor", 0), 2)
                
                # Convertir fecha a formato legible (ej: 2026-07-31 -> Jul 2026)
                try:
                    fecha_dt = datetime.strptime(fecha_raw, "%Y-%m-%d")
                    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                             "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
                    fecha_str = f"{meses[fecha_dt.month - 1]} {fecha_dt.year}"
                except Exception:
                    fecha_str = fecha_raw
                    
                return {"valor": valor, "fecha": fecha_str}
    except Exception as e:
        print(f"Error fetching inflacion (argentinadatos): {e}")

    return None
