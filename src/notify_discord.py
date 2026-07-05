import os
import aiohttp

async def send_discord_message(data):
    token = os.environ.get("DISCORD_BOT_TOKEN")
    channel_id = os.environ.get("DISCORD_CHANNEL_ID")
    
    if not token or not channel_id:
        print("Falta configurar DISCORD_BOT_TOKEN o DISCORD_CHANNEL_ID en las variables de entorno.")
        return False
        
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    
    embed = {
        "title": "💵 Actualización Dólar Blue",
        "color": 3066993, # Verde
        "fields": [
            {
                "name": "Compra",
                "value": f"${data['compra']}",
                "inline": True
            },
            {
                "name": "Venta",
                "value": f"${data['venta']}",
                "inline": True
            }
        ],
        "footer": {
            "text": "Fuente: Dolarhoy.com"
        },
        "timestamp": data["timestamp"]
    }
    
    payload = {
        "embeds": [embed]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status in (200, 204):
                print("Mensaje de Discord enviado exitosamente.")
                return True
            else:
                resp_text = await response.text()
                print(f"Falló el envío a Discord: {response.status} {resp_text}")
                return False
