import yfinance as yf


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

    resultados = {}

    for ticker, name in tickers_dict.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="7d", auto_adjust=False, actions=False)

            if hist.empty:
                hist = stock.history(period="2d", interval="1d", auto_adjust=False, actions=False)

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
                fast_info = getattr(stock, "fast_info", None)
                if fast_info is not None:
                    last_price = getattr(fast_info, "last_price", None)
                    previous_close = getattr(fast_info, "previous_close", None)
                    if last_price is not None:
                        resultados[name] = {
                            "price": round(float(last_price), 2),
                            "change_pct": _calculate_change_pct(float(last_price), float(previous_close or last_price))
                        }
        except Exception as inner_e:
            print(f"Error procesando {name}: {inner_e}")

    return resultados
