# forms.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class UploadReceiptForm(FlaskForm):
    receipt = FileField('Upload Receipt', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'pdf'], 'Images and PDFs only!')
    ])
    student_id = IntegerField('Student ID')  # Add this field
    submit = SubmitField('Upload')