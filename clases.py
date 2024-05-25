import psycopg2

class database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connection(self):
        self.conection = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = 'V16$',
            database = 'CLASE_IDB')

    def insertar_registro(self, tabla, data):
        try:
            self.connection()
            with self.connection.conection.cursor() as cursor:
                columns = data.keys()