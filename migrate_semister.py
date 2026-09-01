from sqlalchemy import inspect, text
from portal import app, db

NEW_COLUMNS = {
    "semester1_amount": "FLOAT NOT NULL DEFAULT 0",
    "semester1_payment_date": "DATETIME",
    "semester1_payment_status": "VARCHAR(20) NOT NULL DEFAULT 'Pending'",
    "semester2_amount": "FLOAT NOT NULL DEFAULT 0",
    "semester2_payment_date": "DATETIME",
    "semester2_payment_status": "VARCHAR(20) NOT NULL DEFAULT 'Pending'",
}

with app.app_context():
    inspector = inspect(db.engine)
    existing_columns = {
        column["name"] for column in inspector.get_columns("student")
    }

    added = []

    with db.engine.begin() as connection:
        for column_name, column_definition in NEW_COLUMNS.items():
            if column_name not in existing_columns:
                connection.execute(
                    text(
                        f"ALTER TABLE student ADD COLUMN "
                        f"{column_name} {column_definition}"
                    )
                )
                added.append(column_name)

    if added:
        print("Successfully added:")
        for column_name in added:
            print(f"- {column_name}")
    else:
        print("All semester columns already exist. No changes were needed.")
