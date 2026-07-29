import requests

def get_crypto_data():
    """Obtiene precios y variación 24h de criptomonedas clave."""
    cryptos = {
        "bitcoin": "BTC",
        "ethereum": "ETH",
        "solana": "SOL",
        "binancecoin": "BNB",
        "tellor": "TRB",
        "ripple": "XRP"
    }
    
    ids = ",".join(cryptos.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
    
    resultados = {}
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for coin_id, symbol in cryptos.items():
                if coin_id in data:
                    price = data[coin_id].get("usd", 0)
                    change = data[coin_id].get("usd_24h_change", 0)
                    resultados[symbol] = {
                        "price": price,
                        "change_24h": round(change, 2)
                    }
    except Exception as e:
        print(f"Error fetching crypto data: {e}")
        
    return resultados

def get_crypto_dominance():
    """Obtiene la dominancia de BTC y ETH."""
    url = "https://api.coingecko.com/api/v3/global"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            percentages = data.get("data", {}).get("market_cap_percentage", {})
            btc_dom = percentages.get("btc", 0)
            eth_dom = percentages.get("eth", 0)
            return {
                "BTC": round(btc_dom, 2),
                "ETH": round(eth_dom, 2)
            }
    except Exception as e:
        print(f"Error fetching crypto dominance: {e}")
        
    return {"BTC": 0, "ETH": 0}
