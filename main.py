import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Define the FastAPI app
app = FastAPI()

# Replace with your actual Messari API Key
MESSARI_API_KEY = "HKt-U5DixQXcmQs7id9h4xBYuVGWL6PswiKKfX283Rj+SGYq"

# Define the Token data structure
class Token(BaseModel):
    name: str
    symbol: str
    price_usd: float
    price_change_24h: float

# Fetch suspicious tokens related to Solana (or any query)
def get_suspicious_tokens():
    url = "https://data.messari.io/api/v1/assets"
    headers = {
        'Authorization': f'Bearer {MESSARI_API_KEY}',
    }

    # Querying Messari API for Solana-related data
    params = {
        'page': 1,
        'limit': 10,  # Adjust as needed
        'search': 'solana',  # Look for Solana tokens
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        tokens = []
        for asset in data['data']:
            token = Token(
                name=asset['name'],
                symbol=asset['symbol'],
                price_usd=asset['metrics']['market_data']['price_usd'],
                price_change_24h=asset['metrics']['market_data']['percent_change_usd_last_24_hours']
            )
            tokens.append(token)

        return tokens

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Messari API: {e}")
        return []

# API endpoint to fetch suspicious tokens
@app.get("/suspicious-tokens", response_model=List[Token])
async def suspicious_tokens():
    return get_suspicious_tokens()
