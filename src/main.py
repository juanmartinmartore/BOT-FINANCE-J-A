import asyncio
import os
import sys

# Agregar el directorio src al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fetchers.macro import get_dolares, get_dolar_futuro, get_inflacion
from fetchers.crypto import get_crypto_data, get_crypto_dominance
from fetchers.stocks import get_stocks_data
from fetchers.media import get_latest_news, get_latest_videos
from analysis.tradingview import get_technical_analysis
from discord.embed_builder import send_dashboard

async def main():
    print("Iniciando recopilación de datos financieros...")
    
    # 1. Fetch de Medios (Noticias y YouTube)
    print("Obteniendo noticias y videos...")
    news = get_latest_news()
    videos = get_latest_videos()
    
    # 2. Fetch de Datos Macro
    print("Obteniendo datos macroeconómicos...")
    dolares = get_dolares()
    futuro = get_dolar_futuro()
    inflacion = get_inflacion()
    
    # 3. Fetch de Mercados Tradicionales
    print("Obteniendo datos de mercados tradicionales...")
    stocks = get_stocks_data()
    
    # 4. Fetch de Criptomonedas
    print("Obteniendo datos cripto...")
    crypto = get_crypto_data()
    dominance = get_crypto_dominance()
    
    # 5. Fetch de Análisis Técnico (TradingView)
    print("Obteniendo análisis técnico...")
    ta = get_technical_analysis()
    
    # 6. Enviar a Discord
    print("Enviando reporte a Discord...")
    success = await send_dashboard(
        news=news, 
        videos=videos, 
        dolares=dolares, 
        futuro=futuro, 
        inflacion=inflacion, 
        stocks=stocks, 
        crypto=crypto, 
        dominance=dominance, 
        ta=ta
    )
    
    if success:
        print("Flujo completado exitosamente.")
    else:
        print("Hubo un error al enviar el reporte a Discord.")

if __name__ == "__main__":
    asyncio.run(main())
