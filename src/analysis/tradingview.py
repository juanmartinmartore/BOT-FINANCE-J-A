from tradingview_ta import TA_Handler, Interval, Exchange

def get_technical_analysis():
    """Obtiene el resumen técnico de TradingView para varios activos."""
    
    activos = {
        "S&P 500": {"symbol": "SPX", "screener": "america", "exchange": "SP"},
        "Nasdaq": {"symbol": "NDX", "screener": "america", "exchange": "NASDAQ"},
        "Nvidia": {"symbol": "NVDA", "screener": "america", "exchange": "NASDAQ"},
        "YPF": {"symbol": "YPF", "screener": "america", "exchange": "NYSE"},
        "Bitcoin": {"symbol": "BTCUSD", "screener": "crypto", "exchange": "BINANCE"},
        "Ethereum": {"symbol": "ETHUSD", "screener": "crypto", "exchange": "BINANCE"}
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
            resumen = analysis.summary["RECOMMENDATION"]
            
            # Traducir recomendación
            traduccion = {
                "STRONG_BUY": "Fuerte Compra 🟢",
                "BUY": "Compra 🟢",
                "NEUTRAL": "Neutral ⚪",
                "SELL": "Venta 🔴",
                "STRONG_SELL": "Fuerte Venta 🔴"
            }
            
            resultados[nombre] = traduccion.get(resumen, resumen)
        except Exception as e:
            print(f"Error procesando TA para {nombre}: {e}")
            resultados[nombre] = "No disponible"
            
    return resultados
