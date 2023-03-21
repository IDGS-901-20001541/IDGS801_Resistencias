from flask import Flask, render_template, request
import math
import forms
from forms import ResistenciaForm
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
app = Flask(__name__)
app.config['SECRET_KEY'] = "Las resistencias"
csrf.init_app(app)

def calcular_resistencia(banda1, banda2, banda3, tolerancia):
    

    valores = {
        "negro": 0,
        "marron": 1,
        "rojo": 2,
        "naranja": 3,
        "amarillo": 4,
        "verde": 5,
        "azul": 6,
        "violeta": 7,
        "gris": 8,
        "blanco": 9
    }
    english_names = {
        "negro": "black",
        "marron": "brown",
        "rojo": "red",
        "naranja": "orange",
        "amarillo": "yellow",
        "verde": "green",
        "azul": "blue",
        "violeta": "violet",
        "gris": "gray",
        "blanco": "white",
        "oro": "gold",
        "plata": "silver"
    }
    banda1_en = english_names[banda1]
    banda2_en = english_names[banda2]
    banda3_en = english_names[banda3]
    tolerancia_en = english_names[tolerancia]

    valor1 = valores[banda1]
    valor2 = valores[banda2]
    multiplicador = math.pow(10, valores[banda3])
    tolerancia_valor = 0.05 if tolerancia == "oro" else 0.1

    valor = (valor1 * 10 + valor2) * multiplicador
    valor_minimo = valor * (1 - tolerancia_valor)
    valor_maximo = valor * (1 + tolerancia_valor)

    return {
        "colorBanda1": banda1_en,
        "colorBanda2": banda2_en,
        "colorBanda3": banda3_en,
        "colorTolerancia": tolerancia_en,
        "banda1": banda1,
        "banda2": banda2,
        "banda3": banda3,
        "tolerancia": tolerancia,
        "valor": valor,
        "valor_minimo": valor_minimo,
        "valor_maximo": valor_maximo
    }


@app.route('/', methods=['GET'])
def index():
    form = ResistenciaForm()

    with open("valores_guardados.txt", "r") as f:
        valores_guardados = [line.strip().split(",") for line in f]

    resultados_guardados = []
    for valores in valores_guardados:
        if len(valores) == 4:
            resultado_guardado = calcular_resistencia(*valores)
            resultados_guardados.append(resultado_guardado)

    return render_template('resistencias.html', form=form, resultados_guardados=resultados_guardados)


@app.route('/', methods=['POST'])
def calcular():
    form = ResistenciaForm()
    banda1 = request.form['banda1']
    banda2 = request.form['banda2']
    banda3 = request.form['banda3']
    tolerancia = request.form['tolerancia']

    resultado = calcular_resistencia(banda1, banda2, banda3, tolerancia)

    valores_guardados = []
    with open("valores_guardados.txt", "r") as f:
        for line in f:
            valores = line.strip().split(",")
            if len(valores) == 4:
                resultado_guardado = calcular_resistencia(*valores)
                valores_guardados.append(resultado_guardado)

    valores_guardados.append(resultado)

    with open("valores_guardados.txt", "a") as f:
        f.write(",".join([banda1, banda2, banda3, tolerancia]) + "\n")

    return render_template('resistencias.html', resultado=resultado, form=form, valores_guardados=valores_guardados)

if __name__ == '__main__':
    app.run(debug=True)