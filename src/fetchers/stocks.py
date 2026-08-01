import yfinance as yf
import requests

def _calculate_change_pct(today_price, yesterday_price):
    if not yesterday_price:
        return 0.0
    return round(((today_price - yesterday_price) / yesterday_price) * 100, 2)

def get_stocks_data():
    """Obtiene precios y variación diaria de índices y acciones clave."""
    tickers_dict = {
        "^GSPC": "S&P 500",
        "^IXIC": "Nasdaq",
        "NVDA": "Nvidia",
        "YPF": "YPF"
    }

    # Creamos una sesión falsa para evitar el bloqueo de Yahoo Finance
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })

    resultados = {}

    for ticker, name in tickers_dict.items():
        try:
            # Pasamos la sesión al Ticker
            stock = yf.Ticker(ticker, session=session)
            # Simplificamos la llamada para evitar problemas de parámetros obsoletos
            hist = stock.history(period="5d")

            if not hist.empty:
                closes = hist["Close"].dropna()
                if len(closes) >= 2:
                    today_price = float(closes.iloc[-1])
                    yesterday_price = float(closes.iloc[-2])
                    resultados[name] = {
                        "price": round(today_price, 2),
                        "change_pct": _calculate_change_pct(today_price, yesterday_price)
                    }
                elif len(closes) == 1:
                    resultados[name] = {
                        "price": round(float(closes.iloc[0]), 2),
                        "change_pct": 0.0
                    }
            else:
                print(f"⚠️ Yahoo devolvió datos vacíos para {name}")
                
        except Exception as inner_e:
            print(f"🚨 Error de red procesando {name}: {inner_e}")

    return resultados
