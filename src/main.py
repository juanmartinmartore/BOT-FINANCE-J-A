import asyncio
import os
import csv
from fetch_price import get_dollar_blue
from notify_discord import send_discord_message
import yaml

def get_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, 'src', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_to_csv(data):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'data', 'dollar_history.csv')
    
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'compra', 'venta'])
        writer.writerow([data['timestamp'], data['compra'], data['venta']])

async def main():
    print("Obteniendo cotización de Dólar Blue...")
    data = await get_dollar_blue()
    
    if data:
        print(f"Cotización obtenida: Compra ${data['compra']} | Venta ${data['venta']}")
        save_to_csv(data)
        
        print("Enviando notificación a Discord...")
        await send_discord_message(data)
    else:
        print("No se pudo obtener la cotización. Revisar la lógica de scraping.")

if __name__ == "__main__":
    asyncio.run(main())
