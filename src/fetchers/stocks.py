import yfinance as yf
import requests

def get_stocks_data():
    """Obtiene precios y variación diaria de índices y acciones clave."""
    tickers_dict = {
        "^GSPC": "S&P 500",
        "^IXIC": "Nasdaq",
        "NVDA": "Nvidia",
        "YPF": "YPF"
    }
    
    resultados = {}
    
    # 1. Creamos una sesión "disfrazada" de navegador web
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    })
    
    try:
        for ticker, name in tickers_dict.items():
            try:
                # 2. Pasamos la sesión a yfinance
                stock = yf.Ticker(ticker, session=session)
                hist = stock.history(period="5d")
                
                if not hist.empty and len(hist) >= 2:
                    today_price = hist['Close'].iloc[-1]
                    yesterday_price = hist['Close'].iloc[-2]
                    
                    change_pct = ((today_price - yesterday_price) / yesterday_price) * 100
                    resultados[name] = {
                        "price": round(float(today_price), 2),
                        "change_pct": round(float(change_pct), 2)
                    }
            except Exception as inner_e:
                print(f"Error procesando {name}: {inner_e}")
                    
    except Exception as e:
        print(f"Error general en get_stocks_data: {e}")
        
    return resultados
    
