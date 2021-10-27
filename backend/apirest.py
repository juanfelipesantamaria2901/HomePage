#!flask/bin/python
from flask import abort
from flask import request

from flask import render_template
from flask.typing import StatusCode
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask,jsonify,send_from_directory
from marshmallow import Schema, fields
from datetime import date

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
    fecha_creacion = request.json["fecha_creacion"]
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
