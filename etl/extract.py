import requests
import pandas as pd
from datetime import datetime

def fetch_exchange_rates(base="USD"):
    url = f"https://api.frankfurter.app/latest?from={base}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    data = response.json()
    
    if "rates" not in data:
        raise Exception(f"Unexpected API response: {data}")
    
    rates = data["rates"]
    df = pd.DataFrame(list(rates.items()), columns=["currency", "rate"])
    df["base"] = base
    df["date"] = data.get("date", datetime.utcnow().strftime("%Y-%m-%d"))
    df["fetched_at"] = datetime.utcnow()
    return df

if __name__ == "__main__":
    df = fetch_exchange_rates()
    print(df.head())
