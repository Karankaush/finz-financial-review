from io import BytesIO

import pandas as pd
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


REQUIRED_COLUMNS = {
    "Transaction ID",
    "Date",
    "Description",
    "Counterparty",
    "Amount",
    "Method",
}


def ingest_transactions(
    file_content: bytes,
    db: Session,
) -> int:

    dataframe = pd.read_excel(
        BytesIO(file_content)
    )

    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    transactions = []

    for _, row in dataframe.iterrows():

        transaction = Transaction(
            transaction_id=str(row["Transaction ID"]),
            date=pd.to_datetime(row["Date"]).date(),
            description=str(row["Description"]),
            counterparty=str(row["Counterparty"]),
            amount=row["Amount"],
            method=str(row["Method"]),
        )

        transactions.append(transaction)

    db.add_all(transactions)
    db.commit()

    return len(transactions)