from flask import Flask, render_template, request, redirect
import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host='localhost',
            user = 'postgres',
            password = "V16$",
            database = "Proyecto"
        )

        self.cursor = self.conn.cursor()

    def insertar_registro(self, table, data):
        try:
            columns = data.keys()
            values = tuple(data[column] for column in columns)

            for value in values:
                print(f"Value: {value}, type: {type(value)}")

            insert_query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
     

            print(insert_query)
            print(values)

            self.cursor.execute(insert_query, values)
            self.conn.commit()
        except Exception as e:
            print(f"Error en ingresar el registro: {e}")
    
    def close_connection(self):
            self.cursor.close()
            self.conn.close()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/alumnos')
def alumnos():
    return render_template("alumnos.html")

@app.route('/profesores')
def profesores():
    return render_template("profesores.html")

@app.route('/cursos')
def cursos():
    return render_template("cursos.html") 

@app.route('/alumnos/agregar_alumno', methods=['GET', 'POST'])

def agregar_alumno():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = str(request.form['edad'])

        print(f"Nombre: {nombre}, type: {type(nombre)}")
        print(f"Nombre: {apellido}, type: {type(apellido)}")
        print(f"Nombre: {edad}, type: {type(edad)}")

        bd = Database()
    
        data = {
            'nombre': nombre,
            'apellido': apellido,
            'edad': edad
        }

        print(data)

        bd.insertar_registro('alumnos', data)
        return redirect('/alumnos')
    return render_template("agregar_alumno.html")

if __name__ == '__main__':
    app.run(debug=True)
    bd = Database()
    bd.close_connection()