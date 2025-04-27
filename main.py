from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your Messari API Key
MESSARI_API_KEY = "HKt-U5DixQXcmQs7id9h4xBYuVGWL6PswiKKfX283Rj+SGYq"

@app.get("/suspicious-tokens")
def suspicious_tokens():
    headers = {"x-api-key": MESSARI_API_KEY}

    solana_assets = requests.get(
        "https://api.messari.io/v2/assets?fields=id,slug,symbol,metrics/market_data/price_usd,metrics/market_data/percent_change_usd_last_24_hours",
        headers=headers
    ).json()

    suspicious = []

    if "data" in solana_assets:
        for asset in solana_assets["data"]:
            if asset.get("slug", "").lower().startswith("solana"):  # Only Solana ecosystem tokens
                price_change = asset["metrics"]["market_data"]["percent_change_usd_last_24_hours"]

                # Mark token as suspicious if price spike is too high or too low
                if price_change is not None and (price_change > 50 or price_change < -50):
                    suspicious.append({
                        "name": asset["slug"],
                        "symbol": asset["symbol"],
                        "price_change_24h": price_change,
                        "price_usd": asset["metrics"]["market_data"]["price_usd"],
                    })

    return {"suspicious_tokens": suspicious}
