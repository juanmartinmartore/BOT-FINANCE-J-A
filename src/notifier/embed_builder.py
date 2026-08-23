import os
import aiohttp
from datetime import datetime, timezone, timedelta
from fetchers.macro import fmt_ar

# Zona horaria Argentina (UTC-3)
AR_TZ = timezone(timedelta(hours=-3))

def _get_next_inflation_date():
    """Calcula la fecha del próximo dato de inflación (mitad del próximo mes)."""
    hoy = datetime.now(AR_TZ)
    # Asumimos que sale aprox el 14 de cada mes
    if hoy.day < 14:
        prox_fecha = hoy.replace(day=14)
    else:
        # Próximo mes
        mes = hoy.month + 1 if hoy.month < 12 else 1
        año = hoy.year if hoy.month < 12 else hoy.year + 1
        prox_fecha = hoy.replace(year=año, month=mes, day=14)
    
    return prox_fecha.strftime("%d/%m")

async def send_dashboard(news, videos, dolares, futuro, inflacion, bcra, stocks, crypto, dominance, ta, hora_actual):
    """Construye y envía los embeds a Discord."""
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

    embeds = []

    # Embed 1: Noticias (Mantenemos diseño)
    desc_news = "\n\n".join(news + videos) if (news or videos) else "No hay noticias disponibles."
    embeds.append({
        "title": "📰 Últimas Noticias",
        "description": desc_news,
        "color": 10181046 # Purple
    })
    
    # Embed 2: BCRA (Nuevo, imitando Twitter)
    if bcra:
        desc_bcra = "🏛️ **PRINCIPALES VARIABLES**\n─────────────\n"
        for nombre, datos in bcra.items():
            valor_fmt = fmt_ar(datos['valor'], 2)
            # Para reservas y similares, quitar decimales para que quede más limpio si es muy grande
            if datos['valor'] > 1000:
                valor_fmt = fmt_ar(datos['valor'], 0)
            
            if "BADLAR" in nombre or "TM20" in nombre:
                desc_bcra += f"**{valor_fmt}%** | {nombre}\n"
            else:
                desc_bcra += f"**{valor_fmt}** | {nombre}\n"
        
        embeds.append({
            "author": {
                "name": "Banco Central de la República Argentina",
                "icon_url": "https://pbs.twimg.com/profile_images/1422591605559881734/O3aM9G8T_400x400.jpg"
            },
            "description": desc_bcra,
            "color": 2261623 # Teal del BCRA aprox
        })

    # Embed 3: Termómetro Argentino
    compra_blue = fmt_ar(dolares.get('Blue', {}).get('compra', 0), 2)
    venta_blue = fmt_ar(dolares.get('Blue', {}).get('venta', 0), 2)
    compra_ofi = fmt_ar(dolares.get('Oficial', {}).get('compra', 0), 2)
    venta_ofi = fmt_ar(dolares.get('Oficial', {}).get('venta', 0), 2)
    venta_ccl = fmt_ar(dolares.get('CCL', {}).get('venta', 0), 2)

    desc_macro = f"💵 **Dólar Blue:**\n> Compra `${compra_blue}` | Venta `${venta_blue}`\n\n"
    desc_macro += f"🏦 **Dólar Oficial:**\n> Compra `${compra_ofi}` | Venta `${venta_ofi}`\n\n"
    desc_macro += f"🏛️ **Dólar CCL:**\n> Venta `${venta_ccl}`\n\n"
    
    # Mostrar dólar futuro apilado verticalmente
    desc_macro += f"📅 **Dólar Futuro (Cierre):**\n"
    if futuro:
        # Reemplazamos el " | " original por un salto de línea y un blockquote
        futuro_formateado = futuro.replace(" | ", "\n> ")
        desc_macro += f"> {futuro_formateado}\n"
    else:
        desc_macro += "> No disponible\n"

    desc_macro += "\n─────────────\n"
    
    if inflacion:
        inflacion_val = fmt_ar(inflacion.get('valor', 0), 1)
        fecha_inf = inflacion.get('fecha', '')
        desc_macro += f"🛒 **Inflación IPC:** `{inflacion_val}%` ({fecha_inf})\n"
        desc_macro += f"> *(Próximo dato estimado: ~{_get_next_inflation_date()})*"
    else:
        desc_macro += "🛒 **Inflación IPC:** Dato demorado"
        
    embeds.append({
        "title": "🇦🇷 Termómetro Argentino",
        "description": desc_macro,
        "color": 3447003 # Blue
    })
    
    # Acciones que cotizan en ARS (bolsa argentina)
    ARS_STOCKS = {"Aluar", "BYMA"}

    # Embed 4: Mercados Tradicionales
    desc_stocks = "*(TA basado en 26 indicadores de TradingView: Osciladores y Medias Móviles)*\n\n"
    for name, data in stocks.items():
        emoji = "🟢" if data['change_pct'] >= 0 else "🔴"
        change_str = fmt_ar(data['change_pct'], 2)
        price_str = fmt_ar(data['price'], 2)
        signo = "+" if data['change_pct'] > 0 else ""
        moneda = "ARS" if name in ARS_STOCKS else "USD"
        ta_data = ta.get(name)

        desc_stocks += f"📈 **{name}**\n"
        desc_stocks += f"> 💵 Precio: `${price_str} {moneda}` ({signo}{change_str}%) {emoji}\n"
        if ta_data:
            rec = ta_data['recomendacion']
            buy, neutral, sell = ta_data['buy'], ta_data['neutral'], ta_data['sell']
            desc_stocks += f"> 📊 Análisis T.: **{rec}** ({buy}↑ {neutral}↔ {sell}↓)\n"
        desc_stocks += "\n"
        
    if desc_stocks == "*(TA basado en 26 indicadores de TradingView: Osciladores y Medias Móviles)*\n\n":
        desc_stocks = "Datos no disponibles."
        
    embeds.append({
        "title": "📈 Mercados Tradicionales",
        "description": desc_stocks.strip(),
        "color": 15105570 # Orange
    })
    
    # Embed 5: Cripto y Dominancia
    btc_dom = dominance.get('BTC', 0)
    eth_dom = dominance.get('ETH', 0)
    resto_dom = max(0, 100 - btc_dom - eth_dom)
    dom_btc_str = fmt_ar(btc_dom, 2)
    dom_eth_str = fmt_ar(eth_dom, 2)
    dom_resto_str = fmt_ar(resto_dom, 2)

    # Dominancia separada del aviso TA
    desc_crypto  = f"📊 **Dominancia del mercado:**\n"
    desc_crypto += f"> 🟡 BTC: `{dom_btc_str}%`\n"
    desc_crypto += f"> 🔵 ETH: `{dom_eth_str}%`\n"
    desc_crypto += f"> 🔷 Resto de altcoins: `{dom_resto_str}%`\n"
    desc_crypto += "\n─────────────\n"
    desc_crypto += "*(TA basado en 26 indicadores de TradingView: Osciladores y Medias Móviles)*\n\n"
    
    for name, data in crypto.items():
        emoji = "🟢" if data['change_24h'] >= 0 else "🔴"
        signo = "+" if data['change_24h'] > 0 else ""
        change_str = fmt_ar(data['change_24h'], 2)

        # Criptos grandes sin decimales, altcoins con decimales
        if data['price'] > 1000:
            price_str = fmt_ar(data['price'], 0)
        else:
            price_str = fmt_ar(data['price'], 2)

        ta_data = ta.get(name)
        desc_crypto += f"🪙 **{name}**\n"
        desc_crypto += f"> 💵 Precio: `${price_str} USDT` ({signo}{change_str}%) {emoji}\n"
        if ta_data:
            rec = ta_data['recomendacion']
            buy, neutral, sell = ta_data['buy'], ta_data['neutral'], ta_data['sell']
            desc_crypto += f"> 📊 Análisis T.: **{rec}** ({buy}↑ {neutral}↔ {sell}↓)\n"
        desc_crypto += "\n"
        
    # Agregamos timestamp al último embed para referencia
    timestamp_ar = datetime.now(AR_TZ).strftime("%d/%m/%Y · %H:%M hs")
    embed_crypto = {
        "title": "🪙 Cripto & Dominancia",
        "description": desc_crypto,
        "color": 16766720, # Yellow
        "footer": {
            "text": f"Datos actualizados al {timestamp_ar}"
        }
    }
    embeds.append(embed_crypto)

    payload = {
        "embeds": embeds
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
