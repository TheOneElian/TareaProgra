from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/clases')
def clases():
    return render_template("clases.html")

@app.route('/empleados')
def empleados():
    return render_template("empleados.html")

@app.route('/horarios/')
def horarios():
    return render_template("horarios.html")

if __name__=='__main__':
    app.run(debug=True)