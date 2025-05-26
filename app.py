from flask import Flask, render_template, request
from core.grafico import resolver_metodo_grafico
from core.simplex_tabla import resolver_simplex_tabla
from core.simplex import resolver_simplex

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metodo_grafico', methods=['GET', 'POST'])
def metodo_grafico():
    resultado = None
    if request.method == 'POST':
        objetivo = request.form['objetivo']
        tipo = request.form['tipo']
        a_list = request.form.getlist('a[]')
        b_list = request.form.getlist('b[]')
        signo_list = request.form.getlist('signo[]')
        rhs_list = request.form.getlist('rhs[]')

        restricciones = []
        for a, b, s, rhs in zip(a_list, b_list, signo_list, rhs_list):
            restricciones.append(f"{a}x1+{b}x2{s}{rhs}")

        restricciones_texto = "\n".join(restricciones)
        resultado = resolver_metodo_grafico(objetivo, restricciones_texto, tipo)

    return render_template('metodo_grafico.html', resultado=resultado)

@app.route('/metodo_simplex', methods=['GET', 'POST'])
def metodo_simplex():
    resultado = None
    if request.method == 'POST':
        objetivo = request.form['objetivo']
        tipo = request.form['tipo']
        a_list = request.form.getlist('a[]')
        b_list = request.form.getlist('b[]')
        signo_list = request.form.getlist('signo[]')
        rhs_list = request.form.getlist('rhs[]')

        restricciones = []
        for a, b, s, rhs in zip(a_list, b_list, signo_list, rhs_list):
            restricciones.append(f"{a}x1+{b}x2{s}{rhs}")

        restricciones_texto = "\n".join(restricciones)
        resultado = resolver_simplex(objetivo, restricciones_texto, tipo)

    return render_template('metodo_simplex.html', resultado=resultado)

@app.route('/metodo_simplex_tabla', methods=['GET', 'POST'])
def metodo_simplex_tabla():
    pasos = []
    valor_optimo = None
    if request.method == 'POST':
        objetivo = request.form['objetivo']
        tipo = request.form['tipo']
        a_list = request.form.getlist('a[]')
        b_list = request.form.getlist('b[]')
        signo_list = request.form.getlist('signo[]')
        rhs_list = request.form.getlist('rhs[]')

        restricciones = []
        for a, b, s, rhs in zip(a_list, b_list, signo_list, rhs_list):
            restricciones.append(f"{a}x1+{b}x2{s}{rhs}")

        restricciones_texto = "\n".join(restricciones)
        pasos, valor_optimo = resolver_simplex_tabla(objetivo, restricciones_texto, tipo)

    return render_template('metodo_simplex_tabla.html', pasos=pasos, valor_optimo=valor_optimo)

if __name__ == '__main__':
    app.run(debug=True)
