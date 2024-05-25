from flask import Flask, render_template, request, redirect
import psycopg2
from psycopg2 import sql

class database:
    def __init__(self, nombre_db,usuario, contraseña,host='localhost'):
        self.nombre_db = nombre_db,
        self.contraseña = contraseña,
        self.host = host,
        self.usuario = usuario


    def connect(self):
        self.connection = psycopg2.connect(
            nombre_db = self.nombre_db,
            contraseña = self.contraseña,
            usuario = self.usuario,
            host = self.host
        )
    
    def close(self):
        if self.connection:
            self.connection.close()

class InsertRecord(database):
    def insert(self, table, data):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                columns =   data.keys()
                values = [data[column] for column in columns]
                insert_query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({values})").format(
                    table=sql.Identifier(table),
                    fields=sql.SQL(',').join(map(sql.Identifier, columns)),
                    values=sql.SQL(',').join(sql.Placeholder() * len(values))
                )
                cursor.execute(insert_query, values)
                self.connection.commit()
        except Exception as e:
            print(f"Error inserting record: {e}")
        finally:
            self.close()

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

if __name__ == '__main__':
    app.run(debug=True)