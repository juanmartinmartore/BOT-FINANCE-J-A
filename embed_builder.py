import os
import aiohttp
from datetime import datetime, timezone

async def send_dashboard(news, videos, dolares, futuro, inflacion, stocks, crypto, dominance, ta):
    """Construye y envía los 4 embeds a Discord."""
    token = os.environ.get("DISCORD_BOT_TOKEN")
    channel_id = os.environ.get("DISCORD_CHANNEL_ID")
    
    if not token or not channel_id:
        print("Falta configurar variables de entorno para Discord.")
        return False

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }

    # Embed 1: Noticias
    desc_news = "\n\n".join(news + videos) if (news or videos) else "No hay noticias disponibles."
    embed_news = {
        "title": "📰 Últimas Noticias",
        "description": desc_news,
        "color": 10181046, # Purple
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Embed 2: Termómetro Argentino
    desc_macro = f"**Dólar Blue:** Compra ${dolares.get('Blue', {}).get('compra', 0)} | Venta ${dolares.get('Blue', {}).get('venta', 0)}\n"
    desc_macro += f"**Dólar Oficial:** Compra ${dolares.get('Oficial', {}).get('compra', 0)} | Venta ${dolares.get('Oficial', {}).get('venta', 0)}\n"
    desc_macro += f"**Dólar CCL:** Venta ${dolares.get('CCL', {}).get('venta', 0)}\n\n"
    desc_macro += f"**Dólar Futuro:** {futuro}\n"
    desc_macro += f"**Inflación IPC:** {inflacion}"
    
    embed_macro = {
        "title": "🇦🇷 Termómetro Argentino",
        "description": desc_macro,
        "color": 3447003 # Blue
    }
    
    # Embed 3: Mercados Tradicionales
    desc_stocks = ""
    for name, data in stocks.items():
        emoji = "📈" if data['change_pct'] >= 0 else "📉"
        ta_status = ta.get(name, "")
        desc_stocks += f"**{name}:** ${data['price']} ({data['change_pct']}%) {emoji} | TA: {ta_status}\n"
    if not desc_stocks: desc_stocks = "Datos no disponibles."
        
    embed_stocks = {
        "title": "📈 Mercados Tradicionales",
        "description": desc_stocks,
        "color": 15105570 # Orange
    }
    
    # Embed 4: Cripto y Dominancia
    desc_crypto = f"**Dominancia:** BTC {dominance.get('BTC', 0)}% | ETH {dominance.get('ETH', 0)}%\n\n"
    for name, data in crypto.items():
        emoji = "📈" if data['change_24h'] >= 0 else "📉"
        ta_status = ta.get(name, "")
        desc_crypto += f"**{name}:** ${data['price']} ({data['change_24h']}%) {emoji}"
        if ta_status:
            desc_crypto += f" | TA: {ta_status}"
        desc_crypto += "\n"
        
    embed_crypto = {
        "title": "🪙 Cripto & Dominancia",
        "description": desc_crypto,
        "color": 16766720 # Yellow
    }

    payload = {
        "embeds": [embed_news, embed_macro, embed_stocks, embed_crypto]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status in (200, 204):
                    print("Dashboard de Discord enviado exitosamente.")
                    return True
                else:
                    resp_text = await response.text()
                    print(f"Falló el envío a Discord: {response.status} {resp_text}")
                    return False
    except Exception as e:
        print(f"Error de red enviando a Discord: {e}")
        return False
