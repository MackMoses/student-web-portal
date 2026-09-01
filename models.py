from flask import Flask, request, send_file, render_template
from sqlalchemy import Column, Integer, String, DateTime, Float
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from forms import UploadReceiptForm
from wtforms.validators import ValidationError
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask import Flask, jsonify, request, session

# ==========================================================
# SHARED DATABASE OBJECT
# ==========================================================

db = SQLAlchemy()

database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///clearance_system.db"
)

login_manager = LoginManager()

# Define User model with UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(200))
    role = db.Column(db.String(50))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_id(self):
        return str(self.id)

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Your existing models
from flask_login import UserMixin

class Student(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)  # Keep as String if needed
    student_id = db.Column(db.Integer, unique=True, nullable=True)  # Optional, for reference
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    school = db.Column(db.String(100), nullable=True, index=True)
    program = db.Column(db.String(100))
    intake = db.Column(db.String(100))
    amount_paid = db.Column(db.Integer, default=0)

    # Health Sciences semester payment fields. These are additive and do not
    # alter the existing Humanities Term 1–3 payment fields.
    semester1_amount = db.Column(db.Float, default=0, nullable=False)
    semester1_payment_date = db.Column(db.DateTime, nullable=True)
    semester1_payment_status = db.Column(db.String(20), default='Pending')
    semester2_amount = db.Column(db.Float, default=0, nullable=False)
    semester2_payment_date = db.Column(db.DateTime, nullable=True)
    semester2_payment_status = db.Column(db.String(20), default='Pending')

    password_hash = db.Column(db.String(128))
    signed_reception = db.Column(db.Boolean, default=False)
    signed_library = db.Column(db.Boolean, default=False)
    signed_admission = db.Column(db.Boolean, default=False)
    signed_accounts = db.Column(db.Boolean, default=False)
    signed_systems = db.Column(db.Boolean, default=False)
    signed_adosa = db.Column(db.Boolean, default=False)
    signed_dean = db.Column(db.Boolean, default=False)
    department_password_hash = db.Column(db.String(128), nullable=True)
    amount_paid_status = db.Column(db.String(20), default='Pending')
    has_downloaded = db.Column(db.Boolean, default=False)
    download_count = db.Column(db.Integer, default=0)
    signature_reception = db.Column(db.Text, nullable=True)
    signature_library = db.Column(db.Text, nullable=True)
    signature_admission = db.Column(db.Text, nullable=True)
    signature_accounts = db.Column(db.Text, nullable=True)
    signature_systems = db.Column(db.Text, nullable=True)
    signature_adosa = db.Column(db.Text, nullable=True)
    clearance_number = db.Column(db.String(30), unique=True)
    verification_code = db.Column(db.String(40), unique=True)
    pdf_generated_date = db.Column(db.DateTime)
    # ==========================================================
# ELECTRONIC SIGNATURES
# ==========================================================
    accounts_signature = db.Column(db.String(255), nullable=True)
    library_signature = db.Column(db.String(255), nullable=True)
    systems_signature = db.Column(db.String(255), nullable=True)
    admissions_signature = db.Column(db.String(255), nullable=True)
    reception_signature = db.Column(db.String(255), nullable=True)
    adosa_signature = db.Column(db.String(255), nullable=True)
    executive_signature = db.Column(db.String(255), nullable=True)
    clearance_type = db.Column( db.String(50),  nullable=True)
    # ==========================================================
# APPROVAL MARKS (CLEAR OR __________)
# ==========================================================
    reception_clear = db.Column(db.String(255), nullable=True)
    library_clear = db.Column(db.String(255), nullable=True)
    admissions_clear = db.Column(db.String(255), nullable=True)
    accounts_clear = db.Column(db.String(255), nullable=True)
    systems_clear = db.Column(db.String(255), nullable=True)
    adosa_clear = db.Column(db.String(255), nullable=True)
    # ==========================================================
# OFFICER INFORMATION - CLEARANCE SIGNING
# ==========================================================

    reception_officer_name = db.Column(
    db.String(150),
    nullable=True
     )

    reception_signed_time = db.Column(
    db.DateTime,
    nullable=True
     )


    library_officer_name = db.Column(
    db.String(150),
    nullable=True
     )

    library_signed_time = db.Column(
    db.DateTime,
    nullable=True
     )


    admissions_officer_name = db.Column(
    db.String(150),
    nullable=True
    )

    admissions_signed_time = db.Column(
    db.DateTime,
    nullable=True
     )


    accounts_officer_name = db.Column(
    db.String(150),
    nullable=True
     )

    accounts_signed_time = db.Column(
    db.DateTime,
    nullable=True
     )


    systems_officer_name = db.Column(
    db.String(150),
    nullable=True
    )

    systems_signed_time = db.Column(
    db.DateTime,
    nullable=True
    )


    adosa_officer_name = db.Column(
    db.String(150),
    nullable=True
     )

    adosa_signed_time = db.Column(
    db.DateTime,
    nullable=True
      )
    
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def progress_percentage(self):
        total_signatures = 6
        signed_fields = [
            self.signed_reception,
            self.signed_library,
            self.signed_admission,
            self.signed_accounts,
            self.signed_systems,
            self.signed_adosa
        ]
        signed_count = sum(1 for signed in signed_fields if signed)
        return (signed_count / total_signatures) * 100

class PasswordResetCode(db.Model):
    __tablename__ = "password_reset_codes"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.String(20),
        db.ForeignKey("student.id"),
        nullable=False,
        index=True
    )
    code_hash = db.Column(db.String(64), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)
    attempts = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    student = db.relationship("Student", backref="password_reset_codes")

# Updated ReceiptNotification model
class ReceiptNotification(db.Model):
    __tablename__ = "receipt_notifications"
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.String(100), nullable=False)
    student_name = db.Column(db.String(255), nullable=False)
    student_email = db.Column(db.String(100), nullable=True)  # Newly added field
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

def create_receipt_notification(receipt, student):
    print(f"Creating notification for student email: {student.email}")  # Debug
    notification = ReceiptNotification(
        receipt_id=receipt.id,
        student_id=student.id,
        student_name=student.name,
        student_email=student.email,  # Should store email here
        message=f"Your receipt {receipt.filename} is ready.",
        is_read=False
    )
    db.session.add(notification)
    db.session.commit()
        # Debug: verify saved data
    print(f"Notification saved with email: {notification.student_email}")

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.String(20),
        db.ForeignKey("student.id")
    )
    student_name = db.Column(db.String(100))
    filename = db.Column(db.String(255))
    status = db.Column(db.String(20), default="pending")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    seen = db.Column(db.Boolean, default=False)
    admin_comment = db.Column(db.Text, nullable=True)

    # Trash/archive fields
    is_deleted = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        index=True
    )
    deleted_at = db.Column(db.DateTime, nullable=True)
    deleted_by = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    student = db.relationship("Student", backref="receipts")
    
class DownloadLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String)
    student_name = db.Column(db.String(100))
    program = db.Column(db.String(100))
    intake = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(10))

# PaymentHistory models
class PaymentHistory(db.Model):
    __tablename__ = 'payment_history'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), db.ForeignKey('student.id'), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20))
    # Stores either Term 1–3 for Humanities or Semester 1–2 for Health Sciences.
    term = db.Column(db.String(20), nullable=False)
    student = db.relationship('Student', backref='payment_histories')

class Term1(db.Model):
    __tablename__ = 'term1'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20))
    term = db.Column(db.String(20), default='Term 1')

class Term2(db.Model):
    __tablename__ = 'term2'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20))
    term = db.Column(db.String(20), default='Term 2')

class Term3(db.Model):
    __tablename__ = 'term3'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20))
    term = db.Column(db.String(20), default='Term 3')


class SystemNotification(db.Model):
    __tablename__ = 'system_notifications'

    id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(100), nullable=True)
    recipient_type = db.Column(db.String(50), nullable=False)
    recipient_id = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    def __repr__(self):
        return f"<SystemNotification {self.title}>"

class ClearanceRequest(db.Model):
    __tablename__ = 'clearance_requests'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<ClearanceRequest {self.student_id}>"

class DepartmentSignature(db.Model):
    __tablename__ = "department_signatures"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False, index=True)
    department = db.Column(db.String(50), nullable=False, index=True)
    signed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "department",
            name="unique_student_department_signature"
        ),
    )

ZAMBIA_TIMEZONE = ZoneInfo("Africa/Lusaka")

def format_zambia_time(value):
    if value is None:
        return ""

    # Your database currently uses datetime.utcnow(), which is a naive UTC time.
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    else:
        value = value.astimezone(timezone.utc)

    # Convert exactly once to Zambia time.
    return value.astimezone(ZAMBIA_TIMEZONE).strftime(
        "%d/%m/%Y, %H:%M"
    )

DEPARTMENTS = (
    "accounts",
    "reception",
    "library",
    "admission",
    "systems",
    "adosa"
)

# 7. Helper function

def record_department_signature(student_id, department):
    old_signature = DepartmentSignature.query.filter_by(
        student_id=str(student_id),
        department=department
    ).first()

    if old_signature:
        return {"created": False}

    new_signature = DepartmentSignature(
        student_id=str(student_id),
        department=department,
        signed_at=datetime.utcnow()
    )

    db.session.add(new_signature)
    db.session.flush()

    student = Student.query.get_or_404(student_id)
    signed_count = DepartmentSignature.query.filter_by(
        student_id=str(student_id)
    ).count()

    complete = signed_count == len(DEPARTMENTS)

    if complete:
        title = "Clearance Complete"
        message = "All six departments have signed your clearance."
    else:
        title = f"{department.title()} Signed Your Clearance"
        message = (
            f"{department.title()} has signed your clearance. "
            f"Progress: {signed_count} of {len(DEPARTMENTS)} departments."
        )

    notification = SystemNotification(
        recipient_type="student",
        recipient_id=str(student_id),
        title=title,
        message=message,
        student_email=student.email,
        is_read=False,
        created_at=datetime.utcnow()
    )

    db.session.add(notification)

    return {
        "created": True,
        "complete": complete,
        "signed_count": signed_count,
        "total_departments": len(DEPARTMENTS)
    }