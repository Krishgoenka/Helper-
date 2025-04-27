from fastapi import FastAPI
import requests
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
import os

app = FastAPI()

# Messari API Key
MESSARI_API_KEY = "HKt-U5DixQXcmQs7id9h4xBYuVGWL6PswiKKfX283Rj+SGYq"
BASE_URL = "https://api.messari.io/v1"

# Headers
headers = {
    "x-messari-api-key": MESSARI_API_KEY
}

# List of Solana ecosystem tokens (you can expand this)
SOLANA_TOKENS = [
    "SOL", "RAY", "SRM", "STEP", "FIDA", "COPE", "MNGO"
]

def fetch_asset_metrics(slug):
    url = f"{BASE_URL}/assets/{slug.lower()}/metrics"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch metrics for {slug}")
        return None

def fetch_social_metrics(slug):
    url = f"{BASE_URL}/assets/{slug.lower()}/profile/social"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch social data for {slug}")
        return None

def analyze_tokens():
    suspicious = []

    for token in SOLANA_TOKENS:
        price_data = fetch_asset_metrics(token)
        social_data = fetch_social_metrics(token)

        if price_data and social_data:
            try:
                price_change = price_data['data']['market_data']['percent_change_usd_last_24_hours']
                social_mentions = social_data['data']['social']['twitter']['followers']
                telegram_members = social_data['data']['social']['telegram']['members_count']

                # Simple suspicion logic
                if price_change > 20:
                    social_spike = telegram_members if telegram_members else 0
                    if social_spike > 100:  # Arbitrary social spike threshold
                        suspicious.append({
                            "token": token,
                            "price_change_24h": price_change,
                            "social_spike": social_spike,
                        })

                        # Save graph
                        save_graph(token, price_change, social_spike)

            except Exception as e:
                print(f"Error analyzing {token}: {e}")
                continue

    return suspicious

def save_graph(token, price_change, social_spike):
    fig, ax = plt.subplots()
    categories = ['Price Change %', 'Social Spike']
    values = [price_change, social_spike]

    ax.bar(categories, values, color=['blue', 'green'])
    ax.set_title(f"Suspicious Activity: {token}")
    ax.set_ylabel('Percentage / Count')

    os.makedirs("graphs", exist_ok=True)
    plt.savefig(f"graphs/{token}_activity.png")
    plt.close()

@app.get("/")
def read_root():
    return {"message": "Messari Solana Fraud Detector API running"}

@app.get("/suspicious-tokens")
def get_suspicious_tokens():
    data = analyze_tokens()
    return {"suspicious_tokens": data}
