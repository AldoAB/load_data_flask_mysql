import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from db_conexion.conexion import mysql_connection

app = Flask(__name__)

# Configuraciones
app.config["DEBUG"] = True
DATASETS = "datasets"
app.config["UPLOAD_FOLDER"] = DATASETS
ALLOWED_EXTENSIONS = ["txt", "csv"]
app.secret_key = '12345'  # esto es necesario para poder usar flash

def allowed_file(filename):
    """Revisar si el archivo tiene una extension valida para ser procesado por el sistema"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_columns(dataframe, expected_columns):
    """Validar si el número de columnas en el dataframe coincide con el número esperado"""
    return len(dataframe.columns) == len(expected_columns)

# Página de bienvenida
@app.route("/")
def index():
    mycursor, mydb = mysql_connection()
    if mydb is None or mycursor is None:
        return "No se pudo conectar a la base de datos."

    try:
        # Obtener conteo de cada tabla
        mycursor.execute('select count(*) from jobs')
        job_count = mycursor.fetchone()[0]

        mycursor.execute('select count(*) from hired_employees')
        employees_count = mycursor.fetchone()[0]

        mycursor.execute('select count(*) from departments')
        departments_count = mycursor.fetchone()[0]
        
    except Exception as e:
        print("HA OCURRIDO UN ERROR")
        print(e)
        return "Error al consultar la base de datos."
        
    finally:
        # Cerrar cursor y conexión
        if mycursor is not None:
            mycursor.close()
        if mydb is not None and mydb.is_connected():
            mydb.close()
        
    return render_template('index.html', job_count=job_count, employees_count=employees_count, departments_count=departments_count)

@app.route("/truncate_table", methods=["POST"])
def truncate_table():
    table_name = request.form.get("table")
    if table_name not in ["jobs", "hired_employees", "departments"]:
        flash("Nombre de tabla no válido.")
        return redirect(url_for("index"))

    try:
        mycursor, mydb = mysql_connection()
        # Verificar el conteo de registros
        conteo_registros_sql = f"select count(*) from {table_name}"
        mycursor.execute(conteo_registros_sql)
        conteo_registros = mycursor.fetchone()[0]  # Obtener el conteo de la primera columna
        
        if conteo_registros == 0:
            flash(f"La tabla {table_name} ya está vacía.")
        else:
            # Truncar la tabla
            truncate_sql = f"truncate table {table_name}"
            mycursor.execute(truncate_sql)
            mydb.commit()
            flash(f"Tabla {table_name} truncada.")
            
    except Exception as e:
        print("HA OCURRIDO UN ERROR")
        print(e)
        flash("Error al truncar la tabla.")
        
    finally:
        if mycursor is not None:
            mycursor.close()
        if mydb is not None and mydb.is_connected():
            mydb.close()
    
    return redirect(url_for("index"))



@app.route("/success")
def success_page():
    return render_template('success.html')

def insert_data_jobs(filePath):
    """Insertar data usando un grupo de 1000 en 1000"""
    batch_size = 1000
    try:
        mycursor, mydb = mysql_connection()
        col_names = ["id", "job"]
        csvData = pd.read_csv(filePath, header=None)

        if not validate_columns(csvData, col_names):
            return False

        # dividimos el dataframe en lotes
        for start in range(0, len(csvData), batch_size):
            end = start + batch_size
            batch = csvData.iloc[start:end]
            
            # Preparar la lista de valores para la inserción
            values = [(row[0] if pd.notna(row[0]) else None,
                       row[1] if pd.notna(row[1]) else None) 
                      for _, row in batch.iterrows()]
            
            sql = "insert into jobs(id, job) VALUES (%s, %s)"
            mycursor.executemany(sql, values)
            mydb.commit()
        
        return True
    except Exception as e:
        print("HA OCURRIDO UN ERROR")
        print(e)
        return False



# Página para cargar archivos de trabajo
@app.route("/job_page", methods=["GET", "POST"])
def job_page():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if not uploaded_file or uploaded_file.filename == "":
            flash("Debe seleccionar un archivo para cargar.")
            return redirect(url_for("job_page"))

        if allowed_file(uploaded_file.filename):
            try:
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                uploaded_file.save(file_path)
                if insert_data_jobs(file_path):
                    return redirect(url_for("index"))
                else:
                    flash("Ha ocurrido un error al intentar cargar el archivo.")
                    return redirect(url_for("job_page"))
            except Exception as e:
                print("HA OCURRIDO UN ERROR")
                print(e)
                flash("Error processing file")
                return redirect(url_for("job_page"))

        extension = os.path.splitext(uploaded_file.filename)[1].lower().strip(".") if uploaded_file.filename else ""
        flash(f"No se puede cargar un archivo con extensión: {extension}")
        return redirect(url_for("job_page"))

    return render_template('job.html')

@app.route("/employees_page", methods=["GET", "POST"])
def employees_page():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if not uploaded_file or uploaded_file.filename == "":
            flash("Debe seleccionar un archivo para cargar.")
            return redirect(url_for("employees_page"))

        if allowed_file(uploaded_file.filename):
            try:
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                uploaded_file.save(file_path)
                if insert_data_employees(file_path):
                    return redirect(url_for("index"))
                else:
                    flash("Ha ocurrido un error al intentar cargar el archivo.")
                    return redirect(url_for("employees_page"))
            except Exception as e:
                print("HA OCURRIDO UN ERROR")
                print(e)
                flash("Error processing file")
                return redirect(url_for("employees_page"))

        extension = os.path.splitext(uploaded_file.filename)[1].lower().strip(".") if uploaded_file.filename else ""
        flash(f"No se puede cargar un archivo con extensión: {extension}")
        return redirect(url_for("employees_page"))

    return render_template('employees.html')

@app.route("/departments_page", methods=["GET", "POST"])
def departments_page():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if not uploaded_file or uploaded_file.filename == "":
            flash("Debe seleccionar un archivo para cargar.")
            return redirect(url_for("departments_page"))

        if allowed_file(uploaded_file.filename):
            try:
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                uploaded_file.save(file_path)
                if insert_data_departments(file_path):
                    return redirect(url_for("index"))
                else:
                    flash("Ha ocurrido un error al intentar cargar el archivo.")
                    return redirect(url_for("departments_page"))
            except Exception as e:
                print("HA OCURRIDO UN ERROR")
                print(e)
                flash("Error processing file")
                return redirect(url_for("departments_page"))

        extension = os.path.splitext(uploaded_file.filename)[1].lower().strip(".") if uploaded_file.filename else ""
        flash(f"No se puede cargar un archivo con extensión: {extension}")
        return redirect(url_for("departments_page"))

    return render_template('departments.html')

def insert_data_jobs(filePath):
    """Inserts data from a CSV file into the jobs table."""
    try:
        mycursor, mydb = mysql_connection()
        col_names = ["id", "job"]
        csvData = pd.read_csv(filePath, header=None)

        if not validate_columns(csvData, col_names):
            return False

        for i, row in csvData.iterrows():
            id_value = row[0] if pd.notna(row[0]) else None
            job_value = row[1] if pd.notna(row[1]) else None
            sql = "INSERT INTO jobs(id, job) VALUES (%s,%s)"
            value = (id_value, job_value)
            mycursor.execute(sql, value)
            mydb.commit()
        return True
    except Exception as e:
        print("HA OCURRIDO UN ERROR")
        print(e)
        return False

def insert_data_employees(filePath):
    """Inserts data from a CSV file into the hired_employees table in batches."""
    batch_size = 1000
    try:
        mycursor, mydb = mysql_connection()
        col_names = ["id", "name", "datetime", "department_id", "job_id"]
        csvData = pd.read_csv(filePath, header=None)

        if not validate_columns(csvData, col_names):
            return False

        # Divide el DataFrame en lotes
        for start in range(0, len(csvData), batch_size):
            end = start + batch_size
            batch = csvData.iloc[start:end]
            
            # Preparar la lista de valores para la inserción
            values = [(row[0] if pd.notna(row[0]) else None,
                       row[1] if pd.notna(row[1]) else None,
                       row[2] if pd.notna(row[2]) else None,
                       row[3] if pd.notna(row[3]) else None,
                       row[4] if pd.notna(row[4]) else None) 
                      for _, row in batch.iterrows()]
            
            sql = "INSERT INTO hired_employees(id, name, datetime, department_id, job_id) VALUES (%s, %s, %s, %s, %s)"
            mycursor.executemany(sql, values)
            mydb.commit()
        
        return True
    except Exception as e:
        print("HA OCURRIDO UN ERROR")
        print(e)
        return False


def insert_data_departments(filePath):
    """Inserts data from a CSV file into the departments table in batches."""
    batch_size = 1000
    try:
        mycursor, mydb = mysql_connection()
        col_names = ["id", "department"]
        csvData = pd.read_csv(filePath, header=None)

        if not validate_columns(csvData, col_names):
            return False

        # Divide el DataFrame en lotes
        for start in range(0, len(csvData), batch_size):
            end = start + batch_size
            batch = csvData.iloc[start:end]
            
            # Preparar la lista de valores para la inserción
            values = [(row[0] if pd.notna(row[0]) else None,
                       row[1] if pd.notna(row[1]) else None) 
                      for _, row in batch.iterrows()]
            
            sql = "INSERT INTO departments(id, department) VALUES (%s, %s)"
            mycursor.executemany(sql, values)
            mydb.commit()
        
        return True
    except Exception as e:
        print("HA OCURRIDO UN ERROR")
        print(e)
        return False


if __name__ == "__main__":
    app.run(port=5000)
