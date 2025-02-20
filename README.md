# usamos flask
para el proyecto se optó por seleccion Flask

# docker instalado de manera local
Docker version 27.1.1, build
docker-compose version 1.29.2

# Creacion de tablas
Las tablas que van a ser cargadas de data deben existir previamente
Para este caso su estructura está indicada en la carpeta "./sql/tables.sql"
# bitacora_tables
es un conjunto de las 3 tablas inciales, pero estás tablas serán cargadas con data de cada vez se cargue data
agregando usuario y fecha de inserción(son tablas de auditoria que se cargan con triggers)

# instalación de paquetes
pip install -r requirements.txt

# base de datos
Para el proyecto se tiene una bd 11.4.2-MariaDB-ubu2404 (docker)
el detalle del contenedor lo encontramos en el dichero docker-compose.yml

# explicación de funcion
cada funcion tiene una breve descripción que explica que hace dicha f.

# recomendación
los campos de las tablas a ser cargadas "deberían" estar todos en tipo text o varchar
ya que son una especie de tablas landing

# carpeta datasets
Archivos de prueba a insertar

# inicio del proyecto
Prueba local: python3 app.py

# funcione validacion de extensiones
allowed_file(filename): para una mejor comprension del tipo de archivos a leer