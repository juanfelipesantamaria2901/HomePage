#!flask/bin/python
# from flask import Flask
from flask import abort
from flask import request

from flask import render_template #Para volver cosas en tipo html, 
# from flask.typing import StatusCode
import bcrypt #Para cifrar las contraseñas
from flask_mysqldb import MySQL
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask,jsonify,send_from_directory
from marshmallow import Schema, fields
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import session #Para las sesiones
from flask_cors import CORS


app = Flask(__name__, instance_relative_config=True)

spec = APISpec( 
    title='Flask-api-swagger-doc',
    version='1.0.0.',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(),MarshmallowPlugin()]
)

# ConfigMySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] = 'pibd'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#INIT MYSQ
mysql= MySQL(app)

#Semilla para cifrado de la contraseña
semilla = bcrypt.gensalt()

#Para permitir CORS
cors = CORS(app)

#Pagina Inicial ----------------------------------------------------------------------------------------------------------------------------------
@app.route('/principal/<numPagina>')
def index(numPagina):
    # numPagina es la pagina actual de la pagina principal. Ej: 1, 2, 3, 4, 5, ...
    
    # Create Cursor
    cur= mysql.connection.cursor()
    
    #Traer 6 registros de la pagina 'numPagina'
    cur.execute("SELECT * FROM proyecto LIMIT %s, 6", ((int(numPagina)-1)*6, ))
    data = cur.fetchall()
    
    cur.close() # Close connection
    
    #Se envian los datos correspondientes a 6 proyectos (de acuerdo a como aparece en la pagina principal 'index.html' desarrollada por el equipo de frontend)
    return jsonify(
        StatusCode = 201,
        message="noError",
        data = data
    ), 201
    
    # return render_template("index.html", data = data) #Retorna a pagina principal


#Registrar nuevo usuario -------------------------------------------------------------------------------------------------------------------------
@app.route('/registerUser', methods=['POST'])
def register_user():

    #Si se envia una peticion POST con nuevo usuario
    if request.method == 'POST':
        #Comprobacion json completo
        if not request.json:
            abort(400)
        # empty_data = False
        for key in request.json:
            if key == '':
                # empty_data = True
                abort(400)
                break

        nombre = request.json["nombre"]
        apellido = request.json["apellido"]
        edad = request.json["edad"]
        sexo = request.json["sexo"]
        identificacion = request.json["identificacion"]
        direccion_residencia = request.json["direccion_residencia"]
        ocupacion = request.json["ocupacion"]
        numero_telefonico = request.json["numero_telefonico"]
        correo_electronico = request.json["correo_electronico"]
        
        #Cifrado de la contraseña
        contrasena = request.json["contrasena"]
        contrasena_encode = contrasena.encode("utf-8")
        contrasena_cifrado = bcrypt.hashpw(contrasena_encode, semilla) #Este es el que almacenamos

        # fecha_creacion = request.json["fecha_creacion"]
        now = datetime.now()
        fecha_creacion = now.strftime('%Y-%m-%d %H:%M:%S')

        estado_usuario = request.json["estado_usuario"]
        nacionalidad = request.json["nacionalidad"]
        ciudad = request.json["ciudad"]

        # Create Cursor
        cur= mysql.connection.cursor()
        
        #Comprobación si existe algun usuario con ese correo
        cur.execute("SELECT correo_electronico FROM usuario WHERE correo_electronico=%s", (correo_electronico, ))

        #Si existe ya un usuario con ese correo
        if cur.rowcount != 0:
            cur.close() # Close connection
            abort(409) #Mensaje de conflictos con correo electronico

        else: #No existe un usuario con ese correo
            # Execute Query
            cur.execute("INSERT INTO usuario(nombre, apellido, edad,sexo,identificacion,direccion_residencia,ocupacion,numero_telefonico,correo_electronico,contrasena,fecha_creacion,estado_usuario,nacionalidad,ciudad) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                    (nombre, apellido, edad,sexo,identificacion,direccion_residencia,ocupacion,numero_telefonico,correo_electronico,contrasena_cifrado,fecha_creacion,estado_usuario,nacionalidad,ciudad))

            # Commit toDB 
            mysql.connection.commit()
                        
            # Close connection
            cur.close()

            return jsonify(
                StatusCode = 201,
                message="noError",
                data = cur.lastrowid
            ), 201

            # return render_template("index.html") #Retorna a pagina principal
    
    return render_template("register.html") #Si no es una peticion entonces simplemente devuelve la pagina para registrarse
    

#Registrar nuevo proyecto -------------------------------------------------------------------------------------------------------------------------
@app.route('/registerProject', methods=['POST'])
def register_proyect():

    #Si se envia una peticion POST con nuevo proyecto
    if request.method == 'POST':
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
        justificacion = request.json["justificacion"]
        objetivos = request.json["objetivos"]
        impacto = request.json["impacto"]
        alineacion_ods = request.json["alineacion_ods"] 
        
        # fecha_creacion = request.json["fecha_creacion"]
        now = datetime.now()
        fecha_creacion = now.strftime('%Y-%m-%d %H:%M:%S')

        #Esta funcion me suma la fecha actual y cantidad de meses para conocer la fecha de culminacion de proyecto
        duracion = request.json["duracion"]
        fecha_finalizacion = datetime.today() + relativedelta(months=duracion) 

        estado = request.json["estado"]
        tipo_proyecto = request.json["tipo_proyecto"]
        url_video = request.json["url_video"]
        url_imagen = request.json["url_imagen"]
        ciudad = request.json["ciudad"]
        donacion_requerida = request.json["donacion_requerida"]
        perfil_colaborador = request.json["perfil_colaborador"]
        recursos = request.json["recursos"] 

        # Create Cursor
        cur= mysql.connection.cursor()

        #Comprobación si existe algun proyecto con el mismo nombre
        cur.execute("SELECT * FROM proyecto WHERE nombre_proyecto=%s", (nombre_proyecto, ))

        #¿Existe un proyecto con el mismo nombre?
        if cur.rowcount != 0: # Si
            cur.close() # Close connection
            abort(409) #Mensaje de conflicto con nombre del proyecto

        else: # No
            # Execute Query
            cur.execute("INSERT INTO proyecto(nombre_proyecto, descripcion, justificacion, objetivos, impacto, alineacion_ods, fecha_creacion, fecha_finalizacion, estado, tipo_proyecto, url_video, url_imagen, ciudad, donacion_requerida, perfil_colaborador, recursos) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                    (nombre_proyecto, descripcion, justificacion, objetivos, impacto, alineacion_ods, fecha_creacion, fecha_finalizacion, estado, tipo_proyecto, url_video, url_imagen, ciudad, donacion_requerida, perfil_colaborador, recursos))
            
            # Commit toDB 
            mysql.connection.commit()
                        
            # Close connection
            cur.close()

            return jsonify(
                StatusCode = 201,
                message="noError",
                data = cur.lastrowid
            ), 201

    # return render_template("register.html") #Si no es una peticion entonces simplemente devuelve la pagina para registrar proyectos (AÚN NO EXISTE ESTA PAGINA)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)