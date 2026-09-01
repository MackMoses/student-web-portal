from portal import app, db, Receipt

with app.app_context():
    latest = Receipt.query.order_by(Receipt.id.desc()).first()

    if latest is None:
        print("NO RECEIPTS FOUND")
    else:
        print("LATEST RECEIPT")
        print("id=", latest.id)
        print("student=", latest.student_id)
        print("filename=", latest.filename)
        print("status=", latest.status)
        print("is_deleted=", repr(latest.is_deleted))
        print("deleted_at=", latest.deleted_at)
