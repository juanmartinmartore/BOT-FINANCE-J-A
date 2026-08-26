# Bot Finanzas Argentina

Bot de Discord automatizado que publica reportes financieros diarios sobre el mercado argentino, criptomonedas, mercados internacionales y noticias de economia. Se ejecuta automaticamente mediante **GitHub Actions**.

---

## Vista Previa

El bot envia un reporte estructurado en bloques visuales directamente a tu canal de Discord:

| Bloque | Contenido |
|---|---|
| Ultimas Noticias | Titulares economicos + videos de YouTube |
| Termometro Argentino | Dolar Blue, Oficial, CCL, Futuro e Inflacion IPC |
| Mercados Tradicionales | Indices y acciones con precio, variacion y Analisis Tecnico |
| Cripto y Dominancia | Dominancia BTC/ETH + precios y Analisis Tecnico |

---

## Caracteristicas

### Noticias y Contenido

- Scraping de **Forbes Argentina** - secciones IA & Big Data y Finanzas
- Scraping de **Infobae Economia** - solo el titular limpio, sin bajada ni autor
- Scraping de **DolarHoy** - filtra publicidades, trae solo noticias reales
- RSS de **Ambito Economia**
- Videos de YouTube de **5 canales**: Joven Inversor, Cripto Norber, Lubruuu, Bull Market e Inverarg
- **Filtro automatico de Shorts** - detecta y descarta videos cortos via HTTP
- **Sistema de deduplicacion** - guarda historial en `data/sent_news.json` para no repetir contenido en el dia

### Termometro Argentino

- **Dolar Blue, Oficial y CCL** en tiempo real (compra y venta) via DolarAPI
- **Dolar Futuro** (contratos ROFEX mes a mes) via Ambito
- **Inflacion IPC** con el ultimo dato oficial y fecha estimada del proximo via ArgentinaDatos

### Mercados Tradicionales

Precios y variacion diaria via Yahoo Finance con **Analisis Tecnico de TradingView** (26 indicadores: RSI, MACD, Medias Moviles, Estocastico, etc.):

| Activo | Ticker | Bolsa | Moneda |
|---|---|---|---|
| Nasdaq | NDX | NASDAQ | USD |
| S&P 500 | SPX | SP | USD |
| Nvidia | NVDA | NASDAQ | USD |
| YPF | YPF | NYSE | USD |
| SpaceX | SPCX | NASDAQ | USD |
| Mercado Libre | MELI | NASDAQ | USD |
| Aluar | ALUA | BCBA | ARS |
| BYMA | BYMA | BCBA | ARS |
| Pampa Energia | PAMP | NYSE | USD |

### Cripto y Dominancia

Dominancia de mercado en tiempo real + precios y variacion 24h via **CoinGecko** con **Analisis Tecnico de TradingView** (Binance):

| Activo | Ticker |
|---|---|
| Bitcoin | BTC |
| Ethereum | ETH |
| Solana | SOL |
| BNB | BNB |
| Tellor | TRB |
| XRP | XRP |

Incluye dominancia de BTC, ETH y porcentaje restante del mercado (Resto de altcoins).

---

## Stack Tecnologico

| Componente | Tecnologia |
|---|---|
| Lenguaje | Python 3.12 |
| Notificaciones | Discord Bot API v10 |
| Datos de mercado | Yahoo Finance API directa + yfinance (fallback) |
| Datos cripto | CoinGecko API publica |
| Analisis Tecnico | tradingview-ta |
| Scraping | requests + BeautifulSoup4 |
| RSS | feedparser |
| Automatizacion | GitHub Actions |
| Datos macro AR | DolarAPI + api.argentinadatos.com |

---

## Configuracion

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia el archivo de ejemplo y completa tus credenciales:

```bash
copy .env.example .env
```

Edita `.env` con tus valores reales:

```env
DISCORD_BOT_TOKEN=tu_token_aqui
DISCORD_CHANNEL_ID=tu_channel_id_aqui
```

> **Importante:** Nunca subas el archivo `.env` al repositorio. Ya esta protegido por el `.gitignore`.

### 4. Configurar GitHub Secrets (produccion)

En tu repositorio de GitHub: **Settings > Secrets and variables > Actions > New repository secret**

| Secret | Descripcion |
|---|---|
| `DISCORD_BOT_TOKEN` | Token de tu bot desde Discord Developer Portal |
| `DISCORD_CHANNEL_ID` | ID del canal de Discord donde el bot publicara |

---

## Uso

### Ejecucion manual (local)

```bash
python src/main.py
```

### Ejecucion automatica (GitHub Actions)

El workflow `.github/workflows/update_price.yml` se puede disparar manualmente desde la pestana **Actions** de GitHub,
o automaticamente a traves de un servicio cron externo que dispare el workflow via la API de GitHub.

Luego de cada ejecucion exitosa, el bot commitea automaticamente el historial `data/sent_news.json`
para que las corridas del dia traigan siempre contenido fresco.

---

## Estructura del Proyecto

```
.
|-- .github/
|   `-- workflows/
|       `-- update_price.yml
|-- data/
|   |-- dollar_history.csv
|   `-- sent_news.json
|-- src/
|   |-- main.py
|   |-- analysis/
|   |   `-- tradingview.py
|   |-- fetchers/
|   |   |-- crypto.py
|   |   |-- macro.py
|   |   |-- media.py
|   |   `-- stocks.py
|   `-- notifier/
|       `-- embed_builder.py
|-- .env.example
|-- .gitignore
|-- requirements.txt
`-- README.md
```

---

## Seguridad

- Ningun token ni credencial esta hardcodeado en el codigo fuente
- Los secrets se manejan exclusivamente via variables de entorno y GitHub Secrets
- El archivo `.env` esta incluido en `.gitignore` para evitar commits accidentales
- Todas las APIs utilizadas son publicas y no requieren autenticacion de terceros
- El historial `data/sent_news.json` contiene unicamente URLs publicas, sin datos personales

---

## Licencia

Este proyecto es de uso personal. Podes adaptarlo libremente para tus propios proyectos.
