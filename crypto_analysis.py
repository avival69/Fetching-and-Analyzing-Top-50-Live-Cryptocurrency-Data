import requests
import pandas as pd
from time import sleep
import openpyxl
from datetime import datetime

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data")
        return []

crypto_data = fetch_crypto_data()


def analyze_data(crypto_data):
    df = pd.DataFrame(crypto_data)

    top_5 = df.nlargest(5, 'market_cap')[['name', 'market_cap']]
    avg_price = df['current_price'].mean()
    highest_change = df.loc[df['price_change_percentage_24h'].idxmax()]
    lowest_change = df.loc[df['price_change_percentage_24h'].idxmin()]

    print("\nTop 5 Cryptos by Market Cap:")
    print(top_5)
    print(f"\nAverage Price of Top 50 Cryptos: ${avg_price:.2f}")
    print(f"\nHighest 24h % Change: {highest_change['name']} ({highest_change['price_change_percentage_24h']}%)")
    print(f"Lowest 24h % Change: {lowest_change['name']} ({lowest_change['price_change_percentage_24h']}%)")

analyze_data(crypto_data)

def update_excel():
    while True:
        crypto_data = fetch_crypto_data()
        df = pd.DataFrame(crypto_data, columns=['name', 'symbol', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h'])
        
        df['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to Excel
        df.to_excel("crypto_live_data.xlsx", index=False)

        print(f"Excel Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        sleep(300)  # Update every 5 minutes

update_excel()