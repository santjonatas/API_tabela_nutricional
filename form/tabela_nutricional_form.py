from flask_wtf import FlaskForm
from wtforms import  StringField, SubmitField
from wtforms.validators import DataRequired


class TabelaNutricionalForm(FlaskForm):
    alimento = StringField('Alimento',
        validators=[DataRequired()
    ])
    submit = SubmitField('Buscar')           


    def to_dict(self) -> dict:
        return {
            'alimento': self.alimento.data
        }