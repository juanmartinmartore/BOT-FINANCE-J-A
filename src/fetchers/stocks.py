import yfinance as yf

def get_stocks_data():
    """Obtiene precios y variación diaria de índices y acciones clave."""
    tickers_dict = {
        "^GSPC": "S&P 500",
        "^IXIC": "Nasdaq",
        "NVDA": "Nvidia",
        "YPF": "YPF"
    }
    
    resultados = {}
    
    try:
        for ticker, name in tickers_dict.items():
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="5d")
                if not hist.empty and len(hist) >= 2:
                    today_price = hist['Close'].iloc[-1]
                    yesterday_price = hist['Close'].iloc[-2]
                    
                    change_pct = ((today_price - yesterday_price) / yesterday_price) * 100
                    resultados[name] = {
                        "price": round(float(today_price), 2),
                        "change_pct": round(float(change_pct), 2)
                    }
                elif not hist.empty and len(hist) == 1:
                    resultados[name] = {
                        "price": round(float(hist['Close'].iloc[0]), 2),
                        "change_pct": 0.0
                    }
            except Exception as inner_e:
                print(f"Error procesando {name}: {inner_e}")
                    
    except Exception as e:
        print(f"Error general en get_stocks_data: {e}")
        
    return resultados
