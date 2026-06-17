from pathlib import Path
import random
from datetime import datetime, timedelta
import pandas as pd

random.seed(42)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUTPUT_PATH = DATA_DIR / "transactions.csv"

CATEGORIES = ["books", "electronics", "clothes", "food", "music", "sport"]
STATUSES = ["paid", "paid", "paid", "paid", "pending", "cancelled", "refunded"]
USERS = [f"u{i:03d}" for i in range(1, 61)]

def generate_transactions(rows_count: int = 600) -> pd.DataFrame:
    start_date = datetime(2026, 5, 1, 8, 0, 0)
    rows = []

    for transaction_id in range(1, rows_count + 1):
        event_time = start_date + timedelta(
            days=random.randint(0, 44),
            hours=random.randint(0, 15),
            minutes=random.randint(0, 59),
        )
        category = random.choice(CATEGORIES)
        status = random.choice(STATUSES)
        amount = round(random.uniform(15, 450), 2)

        if status in ["cancelled", "refunded"]:
            amount = round(amount * random.uniform(0.2, 0.9), 2)

        rows.append(
            {
                "transaction_id": transaction_id,
                "event_time": event_time.strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": random.choice(USERS),
                "category": category,
                "amount": amount,
                "status": status,
            }
        )

    return pd.DataFrame(rows)

if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    df = generate_transactions()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Zapisano plik: {OUTPUT_PATH}")
    print(f"Liczba wierszy: {len(df)}")
    print(df.head())