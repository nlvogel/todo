from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, IntegerField, FloatField, SelectField, FieldList
from wtforms import MultipleFileField, FileField, DateField
from wtforms.validators import DataRequired, URL, Optional
from flask_ckeditor import CKEditorField

class AddTask(FlaskForm):
    name = StringField('Task')
    description = CKEditorField('Task Description')
    date = DateField('Due date')
    submit = SubmitField('Submit Task!')