import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import os
from db_conexion.conexion import mysql_connection
import sys

app = Flask(__name__)

# modo debug
app.config["DEBUG"] = True

# configuraciones iniciales del app
DATASETS= "datasets"
app.config["UPLOAD_FOLDER"] = DATASETS
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "csv"}

# para ser implementado
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#welcome
@app.route("/")
def index():
    return render_template('index.html')

# pagina raiz
@app.route("/job_page")
def job_page():
    return render_template('job.html')

# paginas para cada fichero historico
@app.route('/employees_page')
def employees_page():
    return render_template('employees.html')

@app.route('/departments_page')
def departments_page():
    return render_template('departments.html')

@app.route("/cargar_data_server")
def cargar_data_server():
    return render_template("index.html")

# 1- carga data jobs dentro de la bd 
@app.route("/job_page", methods=["POST"])
def upload_job():
    uploaded_file = request.files["file"]

    if uploaded_file.filename != "":
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
        uploaded_file.save(file_path)
        insert_data_jobs(file_path)
    return redirect(url_for("index"))

def insert_data_jobs(filePath):
    mycursor, mydb = mysql_connection()
    col_names = ["id", "job"]
    csvData = pd.read_csv(filePath, names=col_names, header=None)

    for i, row in csvData.iterrows():
        # Verificar cada valor antes de realizar la inserción
        id_value = row["id"] if pd.notna(row["id"]) else None
        job_value = row["job"] if pd.notna(row["job"]) else None
        sql = "INSERT INTO jobs(id, job) VALUES (%s,%s)"
        value = (id_value, job_value)
        mycursor.execute(sql, value)
        mydb.commit()

# 2- carga data hired_employees dentro de la bd 
@app.route("/employees_page", methods=["POST"])
def upload_employees():
    uploaded_file = request.files["file"]
    try:
        if uploaded_file.filename != "":
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
            uploaded_file.save(file_path)
            insert_data_employees(file_path)
        return redirect(url_for("index"))
    except Exception as e:
        print("HA OCURRIDO UN ERROR")
        print(e)
        return None

def insert_data_employees(filePath):
    try:
        mycursor, mydb = mysql_connection()
        col_names = ["id", "name", "datetime", "department_id", "job_id"]
        csvData = pd.read_csv(filePath, names=col_names, header=None)

        for i, row in csvData.iterrows():
            # Verificar cada valor antes de realizar la inserción
            id_value = row["id"] if pd.notna(row["id"]) else None
            name_value = row["name"] if pd.notna(row["name"]) else None
            datetime_value = row["datetime"] if pd.notna(row["datetime"]) else None
            department_id_value = row["department_id"] if pd.notna(row["department_id"]) else None
            job_id_value = row["job_id"] if pd.notna(row["job_id"]) else None
            sql = "INSERT INTO hired_employees(id, name, datetime, department_id, job_id) VALUES (%s,%s,%s,%s,%s)"
            value = (id_value, name_value, datetime_value, department_id_value, job_id_value)

            mycursor.execute(sql, value)
            mydb.commit()
    except Exception as e:
        print("HA OCURRIDO UN ERROR")
        print(e)
        return None


# 3- carga data departments dentro de la bd 
@app.route("/departments_page", methods=["POST"])
def upload_departments():
    uploaded_file = request.files["file"]
    try:
        if uploaded_file.filename != "":
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
            uploaded_file.save(file_path)
            insert_data_departments(file_path)
        return redirect(url_for("index"))
    except Exception as e:
        print("HA OCURRIDO UN ERROR")
        print(e)
    

def insert_data_departments(filePath):
    mycursor, mydb = mysql_connection()
    col_names = ["id", "department"]
    csvData = pd.read_csv(filePath, names=col_names, header=None)

    for i, row in csvData.iterrows():
        # Verificar cada valor antes de realizar la inserción
        id_value = row["id"] if pd.notna(row["id"]) else None
        department_value = row["department"] if pd.notna(row["department"]) else None
        sql = "INSERT INTO departments(id, department) VALUES (%s,%s)"
        value = (id_value, department_value)
        mycursor.execute(sql, value)
        mydb.commit()


if __name__ == "__main__":
    app.run(port=5000)