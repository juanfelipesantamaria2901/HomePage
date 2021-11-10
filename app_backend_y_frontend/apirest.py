#!flask/bin/python
# from flask import Flask
from flask import abort
from flask import request

from flask import Flask, render_template, url_for, flash, redirect #Para volver cosas en tipo html, 
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
from datetime import timedelta #Para el tiempo en que dura una sesion activa
from dateutil.relativedelta import relativedelta
from flask import session #Para las sesiones
from flask_cors import CORS #Importanción CORS para resolver problema de Espinosa

app = Flask(__name__, instance_relative_config=True)

spec = APISpec( 
    title='Flask-api-swagger-doc',
    version='1.0.0.',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(),MarshmallowPlugin()]
)

# ConfigMySQL
app.config['MYSQL_HOST'] = 'localhost'

#CREDENCIALES Espinosa
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] =''

#CREDENCIALES Geyner
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '1006'

#CREDENCIALES Julián y Daniel
app.config['MYSQL_USER'] = 'dev'
app.config['MYSQL_PASSWORD'] ='d4ab5621'

app.config['MYSQL_DB'] = 'green_project_bd'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#INIT MYSQ
mysql= MySQL(app)

#Semilla para cifrado de la contraseña
semilla = bcrypt.gensalt()

#Para permitir CORS
cors = CORS(app)

#Establezco la llave secreta
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5) #Duracion de la sesion


#Pagina Inicial ----------------------------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET','POST'])
@app.route('/principal', methods=['GET','POST']) #Este metodo depende que los de frontend hagan que esos botones inferiores de cambio de página envien un json
def index():
    
    #Si se envia una peticion POST con nuevo usuario
    if request.method == 'POST':
        #Metodo POST porque la pagina principal permite cambiar el numero de la pagina en la parte inferior para consultar más proyectos. Ej: 1, 2, 3, 4, 5, ...

        numPagina = request.json["numPagina"]

        # Create Cursor
        cur= mysql.connection.cursor()
        
        #Traer 6 registros de la pagina 'numPagina' (6 registros porque de acuerdo a la pagina index.html se pueden desplegar 6 registros por página)
        cur.execute("SELECT * FROM proyecto LIMIT %s, 6", ((int(numPagina)-1)*6, ))
        data = cur.fetchall()
        
        cur.close() # Close connection
    
        #En caso que no haya enviado una petición POST verificamos si ya existe una sesión
        if 'correo' in session:
            #Cargar pagina principal
            return render_template("index.html", data = data) #Retorna a pagina principal con los datos solicitados

        else: #Si no hay sesión activa    
            return redirect("login")

    #En caso que no haya enviado una petición POST verificamos si ya existe una sesión
    if 'correo' in session:
        #Cargar pagina principal
        jsonify(
            StatusCode = 201,
            message="Esta es la pagina principal"
        ), 201
        return render_template("index.html")

    else: #Si no hay sesión activa    
        return redirect("login")


#Página de inicio de sesión -----------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET','POST'])
def login():

    #Si se envia una peticion POST para inicio de sesion
    if request.method == 'POST':
        correo_electronico = request.form['correo']
        contrasena = request.form['contrasena']
        
        contrasena_encode = contrasena.encode("utf-8")

        # Create Cursor
        cur= mysql.connection.cursor()
        
        #Comprobación si existe algun usuario con ese correo
        cur.execute("SELECT * FROM USUARIO WHERE correo_electronico=%s", (correo_electronico, ))

        #Almacenamos el dato en otra variables
        usuario = cur.fetchone()

        #Cierro la consulta
        cur.close()

        #Verificamos si obtuvo datos
        if(usuario != None):
            #Obtenemos el password en encode
            contrasena_bd_cifrada_encode = usuario['contrasena'].encode()
            
            #Verificamos la contraseña
            if(bcrypt.checkpw(contrasena_encode, contrasena_bd_cifrada_encode)):
                #Registrar sesión con el correo ingresado
                session['correo'] = correo_electronico

                #Redirige a la página principal
                return render_template("index.html")
            
            else:
                return jsonify(
                    StatusCode = 201,
                    message="Contraseña incorrecta"
                ), 201

        else:#Significa que no encontro algun usuario con ese correo
            #Mensaje de flask
            return jsonify(
                StatusCode = 201,
                message="El correo no existe"
            ), 201

            #Redirige a la misma página para refrezcar los campos
            return render_template("login.html")

    #En caso que no haya enviado una petición POST verificamos si ya existe una sesión
    if 'correo' in session:
        #Cargar pagina principal
        return redirect(url_for('index'))

    else: #Si no hay sesión activa  
        return render_template("login.html")

#Cerrar sesion ------------------------------------------------------------------------------------------------------------------------------------
@app.route('/logout', methods=['GET'])
def logout():
    #Limpiar sesiones
    session.clear()

    #Mandar a que inicie sesion otra vez
    return render_template('login.html')

#Página registrar nuevo usuario -------------------------------------------------------------------------------------------------------------------------
@app.route('/registerUser', methods=['GET','POST'])
def registerUser():

    #Si se envia una peticion POST con nuevo usuario
    if request.method == 'POST':

        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        edad = request.form["edad"]
        sexo = request.form["sexo"]
        #tipo_usuario = request.form["tipo_usuario"]
        tipo_usuario = "Proponente"
        identificacion = request.form["identificacion"]
        direccion_residencia = request.form["direccion_residencia"]
        ocupacion = request.form["ocupacion"]
        numero_telefonico = request.form["numero_telefonico"]
        correo_electronico = request.form["correo_electronico"]
        
        #Cifrado de la contraseña
        contrasena = request.form["contrasena"]
        contrasena_encode = contrasena.encode("utf-8")
        contrasena_cifrado = bcrypt.hashpw(contrasena_encode, semilla) #Este es el que almacenamos

        # fecha_creacion = request.json["fecha_creacion"]
        now = datetime.now()
        fecha_creacion = now.strftime('%Y-%m-%d %H:%M:%S')

        estado_usuario = 1
        nacionalidad = request.form["nacionalidad"]
        ciudad = request.form["ciudad"]

        # Create Cursor
        cur= mysql.connection.cursor()
        
        #Comprobación si existe algun usuario con ese correo
        cur.execute("SELECT correo_electronico FROM USUARIO WHERE correo_electronico=%s", (correo_electronico, ))

        #Si existe ya un usuario con ese correo
        if cur.rowcount != 0:
            cur.close() # Close connection
            return jsonify(
                StatusCode = 201,
                message="Ya existe un usuario asociado a este correo electrónico"
            ), 201

        else: #No existe un usuario con ese correo
            # Execute Query
            cur.execute("INSERT INTO USUARIO(nombre, apellido, edad,sexo,tipo_usuario,identificacion,direccion_residencia,ocupacion,numero_telefonico,correo_electronico,contrasena,fecha_creacion,estado_usuario,nacionalidad,ciudad) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                    (nombre, apellido, edad,sexo,tipo_usuario,identificacion,direccion_residencia,ocupacion,numero_telefonico,correo_electronico,contrasena_cifrado,fecha_creacion,estado_usuario,nacionalidad,ciudad))

            # Commit toDB 
            mysql.connection.commit()
                        
            # Close connection
            cur.close()
    
            #Establecemos una sesion para este nuevo usuario
            session['correo'] = correo_electronico

            return redirect("principal") #Retorna a pagina principal
 
    return render_template("register.html") #Si no es una peticion entonces simplemente devuelve la pagina para registrarse

#Registrar nuevo proyecto -------------------------------------------------------------------------------------------------------------------------
@app.route('/registerProject', methods=['POST'])
def registerProject():

    #Si se envia una peticion POST con nuevo proyecto
    if request.method == 'POST':
        #Comprobacion json completo
        if not request.json:
            return jsonify(
                StatusCode = 201,
                message="Se requiere enviar un Json por favor"
            ), 201
        # empty_data = False
        for key in request.json:
            if key == '':
                # empty_data = True
                return jsonify(
                    StatusCode = 201,
                    message="No se completaron todos los campos"
                ), 201

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
            return jsonify(
                StatusCode = 201,
                message="Ya existe un proyecto con este nombre"
            ), 201

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

    
#Editar información personal -------------------------------------------------------------------------------------------------------------------------
@app.route('/informacion-personal',methods=['GET','PUT'])
def informacion_personal():
            
    #En el caso que sea metodo PUT
    if request.method == 'PUT':

        #Comprobacion json completo
        if not request.json:
            return jsonify(
                StatusCode = 201,
                message="Se requiere enviar un Json por favor"
            ), 201

        # empty_data = False
        for key in request.json:
            if key == '':
                # empty_data = True
                return jsonify(
                    StatusCode = 201,
                    message="No se completaron todos los campos"
                ), 201

        nombre = request.json['nombre']
        apellido = request.json['apellido']
        edad = request.json['edad']
        identificacion = request.json['identificacion']
        ciudad = request.json['ciudad']
        correo = request.json['correo_electronico']
        direccion_residencia = request.json['direccion_residencia']
        sexo = request.json['sexo']
        nacionalidad = request.json['nacionalidad']
        numero_telefonico = request.json['numero_telefonico']
        ocupacion = request.json['ocupacion']

        # Create Cursor
        cur= mysql.connection.cursor()

        #Query de la información personal del usuario logueado
        cur.execute("update usuario set nombre=%s,apellido=%s,edad=%s,identificacion=%s,ciudad=%s,direccion_residencia=%s,sexo=%s,nacionalidad=%s,numero_telefonico=%s,ocupacion=%s where correo_electronico=%s",
                (nombre,apellido,edad,identificacion,ciudad,direccion_residencia,sexo,nacionalidad,numero_telefonico,ocupacion,correo))

        # Commit toDB 
        mysql.connection.commit()
                        
        # Close connection
        cur.close()

        return jsonify(
                StatusCode = 201,
                message="Datos actualizados",
            ), 201

        
    #En caso que sea el metodo GET

    #Variable de session del usuario
    username = session['correo']
        
    # Create Cursor
    cur= mysql.connection.cursor()

    #Query de la información personal del usuario logueado
    cur.execute("SELECT * FROM USUARIO WHERE correo_electronico=%s", (username, ))

    #Almacenamos el dato en otra variables
    usuario = cur.fetchone()


    #Cierro la consulta
    cur.close()

    #Verificamos si obtuvo datos
    if(usuario != None):
             
        return jsonify(
            nombre = usuario['nombre'],
            apellido = usuario['apellido'],
            edad = usuario['edad'],
            identificacion = usuario['identificacion'],
            ciudad = usuario['ciudad'],
            direccion_residencia = usuario['direccion_residencia'],
            sexo = usuario['sexo'],
            nacionalidad = usuario['nacionalidad'],
            numero_telefonico = usuario['numero_telefonico'],
            ocupacion = usuario['ocupacion']
        ), 201 

    else: #No
        return jsonify(
            StatusCode = 201,
            message="No se procesaron los datos",
        ), 201

@app.errorhandler(404)
def page_not_fount(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)