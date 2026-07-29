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
        # yfinance permite descargar múltiples tickers a la vez
        tickers_str = " ".join(tickers_dict.keys())
        data = yf.download(tickers_str, period="2d", interval="1d", progress=False)
        
        # 'data' es un DataFrame de Pandas multinivel si hay más de 1 ticker
        if not data.empty and 'Close' in data:
            closes = data['Close']
            
            for ticker, name in tickers_dict.items():
                try:
                    # Obtenemos los últimos dos días válidos
                    ticker_closes = closes[ticker].dropna()
                    if len(ticker_closes) >= 2:
                        today_price = ticker_closes.iloc[-1]
                        yesterday_price = ticker_closes.iloc[-2]
                        
                        change_pct = ((today_price - yesterday_price) / yesterday_price) * 100
                        resultados[name] = {
                            "price": round(today_price, 2),
                            "change_pct": round(change_pct, 2)
                        }
                    elif len(ticker_closes) == 1:
                        resultados[name] = {
                            "price": round(ticker_closes.iloc[0], 2),
                            "change_pct": 0.0
                        }
                except Exception as inner_e:
                    print(f"Error procesando {name}: {inner_e}")
                    
    except Exception as e:
        print(f"Error general en get_stocks_data: {e}")
        
    return resultados
