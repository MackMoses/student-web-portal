from portal import app, Receipt

with app.app_context():
    rows = Receipt.query.order_by(Receipt.id.desc()).all()

    print("ALL RECEIPTS:")
    for row in rows:
        print(
            "id=", row.id,
            "student=", row.student_id,
            "status=", row.status,
            "is_deleted=", repr(row.is_deleted),
            "filename=", row.filename,
        )
