from tradingview_ta import TA_Handler, Interval, Exchange

def get_technical_analysis():
    """Obtiene el resumen técnico de TradingView para varios activos.
    
    Devuelve un dict con el formato:
      { nombre: {"recomendacion": str, "buy": int, "neutral": int, "sell": int} }
    """
    
    activos = {
        # Mercados tradicionales — key debe coincidir con stocks.py
        "S&P 500": {"symbol": "SPX",    "screener": "america", "exchange": "SP"},
        "Nasdaq":  {"symbol": "NDX",    "screener": "america", "exchange": "NASDAQ"},
        "Nvidia":  {"symbol": "NVDA",   "screener": "america", "exchange": "NASDAQ"},
        "YPF":     {"symbol": "YPF",    "screener": "america", "exchange": "NYSE"},
        "Mercado Libre": {"symbol": "MELI", "screener": "america", "exchange": "NASDAQ"},
        "SpaceX":  {"symbol": "SPCX",   "screener": "america", "exchange": "NASDAQ"},
        "Aluar":   {"symbol": "ALUA",   "screener": "argentina", "exchange": "BCBA"},
        "BYMA":    {"symbol": "BYMA",   "screener": "argentina", "exchange": "BCBA"},
        "Pampa Energía": {"symbol": "PAMP", "screener": "america", "exchange": "NYSE"},
        # Cripto — key debe coincidir con crypto.py (símbolos cortos)
        "BTC":     {"symbol": "BTCUSD",  "screener": "crypto", "exchange": "BINANCE"},
        "ETH":     {"symbol": "ETHUSD",  "screener": "crypto", "exchange": "BINANCE"},
        "SOL":     {"symbol": "SOLUSDT", "screener": "crypto", "exchange": "BINANCE"},
        "TRB":     {"symbol": "TRBUSDT", "screener": "crypto", "exchange": "BINANCE"},
        "XRP":     {"symbol": "XRPUSDT", "screener": "crypto", "exchange": "BINANCE"},
        "BNB":     {"symbol": "BNBUSDT", "screener": "crypto", "exchange": "BINANCE"},
    }

    traduccion = {
        "STRONG_BUY":  "Fuerte Compra 🟢",
        "BUY":         "Compra 🟢",
        "NEUTRAL":     "Neutral ⚪",
        "SELL":        "Venta 🔴",
        "STRONG_SELL": "Fuerte Venta 🔴",
    }

    resultados = {}

    for nombre, config in activos.items():
        try:
            handler = TA_Handler(
                symbol=config["symbol"],
                screener=config["screener"],
                exchange=config["exchange"],
                interval=Interval.INTERVAL_1_DAY
            )
            analysis = handler.get_analysis()
            summary  = analysis.summary

            resultados[nombre] = {
                "recomendacion": traduccion.get(summary["RECOMMENDATION"], summary["RECOMMENDATION"]),
                "buy":     summary.get("BUY",     0),
                "neutral": summary.get("NEUTRAL", 0),
                "sell":    summary.get("SELL",    0),
            }
        except Exception as e:
            print(f"Error procesando TA para {nombre}: {e}")
            resultados[nombre] = {
                "recomendacion": "No disponible",
                "buy": 0, "neutral": 0, "sell": 0,
            }

    return resultados
