from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Replace this with your actual database URI
DATABASE_URI = 'sqlite:///your_database.db'  # Example for SQLite
# For other databases (PostgreSQL, MySQL), use their connection string, e.g.:
# 'postgresql://user:password@localhost/dbname'

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'
    id = Column(String(20), primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    program = Column(String(100))
    intake = Column(String(100))
    amount_paid = Column(Integer, default=0)
    password_hash = Column(String(128))
    signed_reception = Column(Boolean, default=False)
    signed_library = Column(Boolean, default=False)
    signed_admission = Column(Boolean, default=False)
    signed_accounts = Column(Boolean, default=False)
    signed_systems = Column(Boolean, default=False)
    signed_adosa = Column(Boolean, default=False)
    department_password_hash = Column(String(128))
    amount_paid_status = Column(String(20), default='Pending')

def main():
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query all students with amount_paid as NULL or None
    students = session.query(Student).filter(Student.amount_paid == None).all()

    print(f"Found {len(students)} students with amount_paid as NULL. Updating to 0...")

    for student in students:
        student.amount_paid = 0

    session.commit()
    print("Update complete.")
    session.close()

if __name__ == '__main__':
    main()