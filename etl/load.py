import os
import pandas as pd
from sqlalchemy import create_engine
from extract import fetch_exchange_rates
from datetime import datetime, timezone

def save_to_db(df):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, "exchange_rates.db")

    engine = create_engine(f"sqlite:///{db_path}")
    df.to_sql("exchange_rates", engine, if_exists="append", index=False)
    print(f"✅ Saved {len(df)} rows to database at {datetime.now(timezone.utc)}")
    print(f"📁 Database path: {db_path}")

if __name__ == "__main__":
    df = fetch_exchange_rates(base="USD")
    save_to_db(df)

