from flask import Flask, render_template, request, redirect
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='V16$',
    database='CLASE_IDB'
)

cursor = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)