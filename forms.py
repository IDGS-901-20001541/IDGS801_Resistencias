from wtforms import  SelectField, RadioField, SubmitField
from flask_wtf import FlaskForm
from wtforms import validators


def mi_validacion(form,field):
    if len(field.data)==0:
        raise validators.ValidationError('El campo esta vacio')
class ResistenciaForm(FlaskForm):
    opciones_banda = [("negro", "Negro"), ("marron", "Marrón"), ("rojo", "Rojo"), ("naranja", "Naranja"),
                      ("amarillo", "Amarillo"), ("verde", "Verde"), ("azul", "Azul"), ("violeta", "Violeta"),
                      ("gris", "Gris"), ("blanco", "Blanco")]

    opciones_tolerancia = [("oro", "Oro"), ("plata", "Plata")]

    banda1 = SelectField("Banda 1", choices=opciones_banda, validators=[validators.DataRequired()])
    banda2 = SelectField("Banda 2", choices=opciones_banda, validators=[validators.DataRequired()])
    banda3 = SelectField("Banda 3", choices=opciones_banda, validators=[validators.DataRequired()])
    tolerancia = RadioField("Tolerancia", choices=opciones_tolerancia, validators=[validators.DataRequired()])
    calcular = SubmitField("Calcular")