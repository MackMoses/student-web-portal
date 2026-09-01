import sqlite3

database_path = r"instance/clearance_system.db"
connection = sqlite3.connect(database_path)

try:
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(receipt)")
    }

    if "is_deleted" not in columns:
        connection.execute(
            "ALTER TABLE receipt "
            "ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT 0"
        )
        print("Added: is_deleted")
    else:
        print("Already exists: is_deleted")

    if "deleted_at" not in columns:
        connection.execute(
            "ALTER TABLE receipt ADD COLUMN deleted_at DATETIME"
        )
        print("Added: deleted_at")
    else:
        print("Already exists: deleted_at")

    if "deleted_by" not in columns:
        connection.execute(
            "ALTER TABLE receipt ADD COLUMN deleted_by VARCHAR(100)"
        )
        print("Added: deleted_by")
    else:
        print("Already exists: deleted_by")

    connection.commit()
    print("Receipt Trash columns are ready.")
finally:
    connection.close()
