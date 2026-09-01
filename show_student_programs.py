from portal import app, Student

with app.app_context():
    rows = Student.query.with_entities(Student.id, Student.program).order_by(Student.id).all()
    for student_id, program in rows:
        print(f"ID={student_id} | PROGRAM={program!r}")
