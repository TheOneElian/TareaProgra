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

    def obtener_registros(self, table):
        try:
            #self.cursor.execute(f"SELECT id, nombre, apellido, edad FROM {table}")
            self.cursor.execute(f"SELECT * FROM {table}")
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return [dict(zip(columns, row)) for row in rows]
            #return self.cursor.fetchall()
        except Exception as e:
            print(f"Error extrayendo registros: {e}")
            return[]

    def editar_registro(self,table, data, condition):
        try:
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            values = tuple(data.values())
            update_query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
            self.cursor.execute(update_query, values)
            print(f"Executing query: {update_query} with values: {values}")
            self.conn.commit()
        except Exception as e:
            print(f"Error al editar registro: {e}")

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

    def eliminar_registro(self, table, condition):
        try:
            delete_query = sql.SQL(
                "DELETE FROM {table} WHERE {condition}"
            ).format(
                table=sql.Identifier(table),
                condition=sql.SQL(condition)
            )
            print(delete_query.as_string(self.conn))
            self.cursor.execute(delete_query)
            self.conn.commit()
        except Exception as e:
            print(f"Error al eliminar: {e}")
        finally:
            self.close_connection()
    
    def close_connection(self):
            self.cursor.close()
            self.conn.close()

app = Flask(__name__)
app.debug=True

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/alumnos')
def alumnos():
    bd = Database()
    alumnos = bd.obtener_registros('alumnos')
    bd.close_connection()
    return render_template("alumnos.html", alumnos=alumnos)

@app.route('/profesores')
def profesores():
    bd = Database()
    profesores = bd.obtener_registros('profesores')
    bd.close_connection()
    return render_template("profesores.html", profesores=profesores)

@app.route('/profesores/eliminar_profesor/id_profesor>', methods=['POST'])
def eliminar_profesor(id_profesor):
    bd = Database()
    condition = f"id_profesor = '{id_profesor}'"
    bd.eliminar_registro('profesores', condition)
    bd.close_connection()
    return redirect('/profesores')

@app.route('/profesores/editar_profesor/<int:id_profesor>', methods=['GET', 'POST'])
def editar_profesor(id_profesor):
    print(f"Editing professor with ID {id_profesor}")
    bd = Database()
    condition = f"id_profesor = {id_profesor}"
    if request.method == 'POST':
        nombre_profesor = request.form['nombre_profesor']
        materia_profesor = request.form['materia_profesor']

        data = {
            'nombre_profesor': nombre_profesor,
            'materia_profesor': materia_profesor
        }

        bd.editar_registro('profesores', data, condition)
        bd.close_connection()
        return redirect('/profesores')
    
    profesor = bd.obtener_registros('profesores')
    print(f"Professors data fetched from database: {profesores}")
    profesor = next((p for p in profesor if p['id_profesor'] == id_profesor), None)
    print(f"Professor data: {profesor}")
    bd.close_connection()

    if not profesor:
        return "Profesor no encontrado", 404
    
    return render_template('editar_profesor.html', profesor=profesor)

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

@app.route('/alumnos/eliminar_alumno/<int:id>', methods=['POST'])
def eliminar_alumno(id):
    bd = Database()
    condition = f"id = {id}"
    bd.eliminar_registro('alumnos', condition)
    return redirect('/alumnos')

@app.route('/cursos/agregar_curso', methods=['GET', 'POST'])
def agregar_curso():
    if request.method == 'POST':
        id_curso = request.form['id_curso']
        nombre_curso = request.form['nombre_curso']

        print(f"Id: {id_curso}, type: {type(id_curso)}")
        print(f"Nombre: {nombre_curso}, type: {type(nombre_curso)}")

        bd = Database()
    
        data = {
            'id_curso': id_curso,
            'nombre_curso': nombre_curso,
        }

        print(data)

        bd.insertar_registro('cursos', data)
        return redirect('/cursos')
    return render_template("agregar_curso.html")

@app.route('/profesores/agregar_profesor', methods=['GET', 'POST'])
def agregar_profesor():
    if request.method == 'POST':
        nombre_profesor = request.form['nombre_profesor']
        materia_profesor = request.form['materia_profesor']

        bd = Database()
    
        data = {
            'nombre_profesor': nombre_profesor,
            'materia_profesor': materia_profesor
        }

        print(data)

        bd.insertar_registro('profesores', data)
        return redirect('/profesores')
    return render_template("agregar_profesor.html")

if __name__ == '__main__':
    app.run(debug=True)
    bd = Database()
    bd.close_connection()