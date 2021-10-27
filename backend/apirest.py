#!flask/bin/python
from flask import abort
from flask import request

from flask import render_template
# from flask.typing import StatusCode
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask,jsonify,send_from_directory
from marshmallow import Schema, fields
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

import flask

app = Flask(__name__, instance_relative_config=True)

spec = APISpec( 
    title='Flask-api-swagger-doc',
    version='1.0.0.',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(),MarshmallowPlugin()]
)

# ConfigMySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'dev'
app.config['MYSQL_PASSWORD'] ='d4ab5621'
app.config['MYSQL_DB'] = 'pibd'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#INIT MYSQ
mysql= MySQL(app)

#Registrar nuevo usuario -------------------------------------------------------------------------------------------------------------------------
@app.route('/registerUser', methods=['POST'])
def register_user():

    if not request.json or not 'nombre' or not 'apellido' in request.json:

        abort(400)

    nombre = request.json["nombre"]
    apellido = request.json["apellido"]
    edad = request.json["edad"]
    sexo = request.json["sexo"]
    identificacion = request.json["identificacion"]
    direccion_residencia = request.json["direccion_residencia"]
    ocupacion = request.json["ocupacion"]
    numero_telefonico = request.json["numero_telefonico"]
    correo_electronico = request.json["correo_electronico"]
    contrasena = int(request.json["contrasena"])
    
    # fecha_creacion = request.json["fecha_creacion"]
    now = datetime.now()
    fecha_creacion = now.strftime('%Y-%m-%d %H:%M:%S')

    estado_usuario = request.json["estado_usuario"]
    nacionalidad = request.json["nacionalidad"]
    ciudad = request.json["ciudad"]

    # Create Cursor
    cur= mysql.connection.cursor()

    # Execute Query
    cur.execute("INSERT INTO usuario(nombre, apellido, edad,sexo,identificacion,direccion_residencia,ocupacion,numero_telefonico,correo_electronico,contrasena,fecha_creacion,estado_usuario,nacionalidad,ciudad) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
            (nombre, apellido, edad,sexo,identificacion,direccion_residencia,ocupacion,numero_telefonico,correo_electronico,contrasena,fecha_creacion,estado_usuario,nacionalidad,ciudad))

    # Commit toDB 
    mysql.connection.commit()
                
    # Close connection
    cur.close()

    return jsonify(
        StatusCode = 201,
        message="noError",
        data = cur.lastrowid
    ), 201

#Registrar nuevo proyecto -------------------------------------------------------------------------------------------------------------------------
@app.route('/registerProject', methods=['POST'])
def register_proyect():

    #Comprobacion json completo
    if not request.json:
        abort(400)
    # empty_data = False
    for key in request.json:
        if key == '':
            # empty_data = True
            abort(400)
            break

    nombre_proyecto = request.json["nombre_proyecto"]
    descripcion = request.json["descripcion"]
    justificacion = request.json["justificacion"] # ** Agregado a los MOCKUPS **
    impacto = request.json["impacto"] # ** Agregado a los MOCKUPS **
    alineacion_ods = request.json["alineacion_ods"] 
    objetivos = request.json["objetivos"] # **Falta en la base de datos**

    # fecha_creacion = request.json["fecha_creacion"]
    now = datetime.now()
    fecha_creacion = now.strftime('%Y-%m-%d %H:%M:%S')

    duracion = int(request.json["duracion"])
    fecha_finalizacion = datetime.today() + relativedelta(months=duracion)

    estado = request.json["estado"]
    tipo_proyecto = request.json["tipo_proyecto"]
    url_video = request.json["url_video"]
    url_imagen = request.json["url_imagen"]
    ciudad = request.json["ciudad"]
    donacion_requerida = int(request.json["donacion_requerida"]) #**Falta en la base de datos**
    perfil_colaborador = request.json["perfil_colaborador"]
    recursos = request.json["recursos"] #**Falta en la base de datos**

    # Create Cursor
    cur= mysql.connection.cursor()

    ''' No se está almacenando en la base de datos "donacion requerida" y "recursos" porque no existen '''
    # Execute Query
    cur.execute("INSERT INTO proyecto(nombre_proyecto, descripcion, justificacion, impacto, alineacion_ods, fecha_creacion, fecha_finalizacion, estado, tipo_proyecto, url_video, url_imagen, ciudad, perfil_colaborador) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
            (nombre_proyecto, descripcion, justificacion, impacto, alineacion_ods, fecha_creacion, fecha_finalizacion, estado, tipo_proyecto, url_video, url_imagen, ciudad, perfil_colaborador))
    
    # Commit toDB 
    mysql.connection.commit()
                
    # Close connection
    cur.close()

    return jsonify(
        StatusCode = 201,
        message="noError",
        data = cur.lastrowid
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
