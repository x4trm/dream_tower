from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired,Email

class MailForm(FlaskForm):
    mail=StringField('Email', validators=[DataRequired(),Email()])
    temat=StringField('Temat',validators=[DataRequired()])
    wiadomosc=TextAreaField('Wiadomosc',validators=[DataRequired()])
    submit=SubmitField('Wyślij')