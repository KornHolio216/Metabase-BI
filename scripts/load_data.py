from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "transactions.csv"

def load_transactions() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Brak pliku {DATA_PATH}. Najpierw uruchom scripts/generate_transactions.py"
        )

    df = pd.read_csv(DATA_PATH)
    df["event_time"] = pd.to_datetime(df["event_time"])

    engine = create_engine(
        "postgresql+pg8000://",
        connect_args={
            "user": "bi",
            "password": "bi",
            "host": "127.0.0.1",
            "port": 5433,
            "database": "ntpd",
        },
    )

    df.to_sql("transactions", engine, if_exists="replace", index=False)

    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE transactions ADD PRIMARY KEY (transaction_id);"))
        rows_count = connection.execute(text("SELECT COUNT(*) FROM transactions;"))
        print("Załadowano wierszy:", rows_count.scalar())

if __name__ == "__main__":
    load_transactions()