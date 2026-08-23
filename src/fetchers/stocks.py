import requests
import yfinance as yf

# Headers que imitan un navegador real para evitar bloqueos de Yahoo Finance
_YAHOO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://finance.yahoo.com"
}


def _get_from_yahoo_direct(ticker):
    """
    Fuente primaria: llama directamente a la API v8 de Yahoo Finance.
    Más estable que yfinance porque no depende de la autenticación interna de la librería.
    """
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
    params = {"interval": "1d", "range": "5d"}
    try:
        resp = requests.get(url, headers=_YAHOO_HEADERS, params=params, timeout=12)
        if resp.status_code != 200:
            print(f"⚠️ Yahoo API directo devolvió {resp.status_code} para {ticker}")
            return None

        data = resp.json()
        result = data.get("chart", {}).get("result")
        if not result:
            return None

        closes = result[0].get("indicators", {}).get("quote", [{}])[0].get("close", [])
        closes = [c for c in closes if c is not None]

        if len(closes) >= 2:
            today = closes[-1]
            yesterday = closes[-2]
            change_pct = round(((today - yesterday) / yesterday) * 100, 2)
            return {"price": round(today, 2), "change_pct": change_pct}
        elif len(closes) == 1:
            return {"price": round(closes[0], 2), "change_pct": 0.0}

    except Exception as e:
        print(f"🚨 Error en Yahoo API directo para {ticker}: {e}")
    return None


def _get_from_yfinance(ticker):
    """
    Fallback: usa la librería yfinance.
    Se mantiene como respaldo por si cambia la estructura de la API directa.
    """
    try:
        session = requests.Session()
        session.headers.update({"User-Agent": _YAHOO_HEADERS["User-Agent"]})
        stock = yf.Ticker(ticker, session=session)
        hist = stock.history(period="5d")
        if not hist.empty:
            closes = hist["Close"].dropna()
            if len(closes) >= 2:
                today = float(closes.iloc[-1])
                yesterday = float(closes.iloc[-2])
                change_pct = round(((today - yesterday) / yesterday) * 100, 2)
                return {"price": round(today, 2), "change_pct": change_pct}
            elif len(closes) == 1:
                return {"price": round(float(closes.iloc[0]), 2), "change_pct": 0.0}
    except Exception as e:
        print(f"🚨 Error en yfinance para {ticker}: {e}")
    return None


def get_stocks_data():
    """Obtiene precios y variación diaria de índices y acciones clave."""
    tickers = {
        # Índices y acciones de EE.UU.
        "Nasdaq":        "^IXIC",
        "S&P 500":       "^GSPC",
        "Nvidia":        "NVDA",
        "YPF":           "YPF",
        "SpaceX":        "SPCX",
        # Brasil/NASDAQ
        "Mercado Libre": "MELI",
        # Argentina
        "Aluar":         "ALUA.BA",
        "BYMA":          "BYMA.BA",
        "Pampa Energía": "PAMP",
    }

    resultados = {}

    for name, ticker in tickers.items():
        # Intento 1: API directa de Yahoo Finance (más confiable)
        data = _get_from_yahoo_direct(ticker)

        # Intento 2: yfinance como fallback
        if data is None:
            print(f"↩️ Usando yfinance como fallback para {name}...")
            data = _get_from_yfinance(ticker)

        if data:
            resultados[name] = data
        else:
            print(f"❌ No se pudo obtener datos para {name} por ninguna fuente.")

    return resultados
