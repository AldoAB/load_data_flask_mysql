import os
import mysql.connector
from dotenv import load_dotenv

def mysql_connection():
    load_dotenv()
    print(load_dotenv)
    config = {
        "host": os.getenv('MYSQL_HOST'),
        "database": os.getenv('MYSQL_DATABASE'),
        "port": os.getenv('MYSQL_PORT'),
        "user": os.getenv('MYSQL_USER'),
        "password": os.getenv('MYSQL_PASSWORD')
    }

    #crear conexion a la bd
    mydb = mysql.connector.connect(**config)

    # validar que se establecio conexion
    if mydb.is_connected():
        db_Info = mydb.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        cursor = mydb.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print(f"Ahora estas conectado a la base de datos:  {record}")

    # crear el objeto cursor, que permite hacer peticiones a la bd
    mycursor = mydb.cursor()
    
    return (mycursor, mydb)