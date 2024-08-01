import os
import mysql.connector
from dotenv import load_dotenv

def mysql_connection():
    load_dotenv()
    config = {
        "host": os.getenv('MYSQL_HOST'),
        "database": os.getenv('MYSQL_DATABASE'),
        "port": os.getenv('MYSQL_PORT'),
        "user": os.getenv('MYSQL_USER'),
        "password": os.getenv('MYSQL_PASSWORD')
    }

    # Crear conexión a la base de datos
    mydb = mysql.connector.connect(**config)

    # Validar que se estableció conexión
    if mydb.is_connected():
        db_Info = mydb.get_server_info()
        print(f"Conectado a la base de datos: {db_Info}")
        cursor = mydb.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"Ahora estamos conectados a la base de datos: {record[0]}")

    # Devolver el cursor y la conexión
    return mydb.cursor(), mydb
