from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, DateTimeField, SelectField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    type = SelectField('Type', choices=[('product', 'Product'), ('service', 'Service')], validators=[DataRequired()])
    time = DateTimeField('Time')
    location = StringField('Location')