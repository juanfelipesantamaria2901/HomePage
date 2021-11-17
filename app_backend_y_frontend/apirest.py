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
#app.permanent_session_lifetime = timedelta(minutes=5) #Duracion de la sesion


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
        if(session['tipo_usuario'] == 'Proponente'):
            # return render_template("index_proponente.html")
            return redirect(url_for('index_proponente'))
        else:
            # return render_template("index_Colaborador.html")
            return redirect(url_for('index_Colaborador'))
    
    else: #Si no hay sesión activa
        cur= mysql.connection.cursor()
        
        #Traer 6 registros de la pagina 'numPagina' (6 registros porque de acuerdo a la pagina index.html se pueden desplegar 6 registros por página)
        cur.execute("SELECT * FROM proyecto")
        
        data = cur.fetchall()
        
        cur.close() # Close connection
    
        return render_template("index.html", data = data)

#Página principal de proponente -----------------------------------------------------------------------------------------------------------------------------
@app.route('/index_proponente', methods=['GET'])
def index_proponente():
    if 'correo' in session:

        cur= mysql.connection.cursor()
        
        #Traer 6 registros de la pagina 'numPagina' (6 registros porque de acuerdo a la pagina index.html se pueden desplegar 6 registros por página)
        cur.execute("SELECT * FROM proyecto")
        
        data = cur.fetchall()
        

        return render_template("index_proponente.html", data = data, data2 = session)

    else:
        return redirect(url_for('index'))

#Página principal de Colaborador -----------------------------------------------------------------------------------------------------------------------------
@app.route('/index_Colaborador', methods=['GET'])
def index_Colaborador():
    if 'correo' in session:

        cur= mysql.connection.cursor()
        
        #Traer 6 registros de la pagina 'numPagina' (6 registros porque de acuerdo a la pagina index.html se pueden desplegar 6 registros por página)
        cur.execute("SELECT * FROM proyecto")
        
        data = cur.fetchall()
        
        cur.close() # Close connection


        return render_template("index_Colaborador.html", data = data, data2 = session)

    else:
        return redirect(url_for('index'))

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
                session['nombre'] = usuario['nombre']
                session['tipo_usuario'] = usuario['tipo_usuario']

                # if (usuario['tipo_usuario'] == 'Proponente'):
                #     return render_template("index_proponente.html")
                # else:
                #     return render_template("index_Colaborador.html")
                return redirect(url_for('index'))
                
            else:
                return jsonify(
                    StatusCode = 201,
                    message="Contraseña incorrecta"
                ), 201

        else:#Significa que no encontro algun usuario con ese correo
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
    return redirect(url_for('index'))

#Página registrar nuevo usuario -------------------------------------------------------------------------------------------------------------------------
@app.route('/registerUser', methods=['GET','POST'])
def registerUser():

    #Si se envia una peticion POST con nuevo usuario
    if request.method == 'POST':

        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        edad = request.form["edad"]
        sexo = request.form["sexo"]
        tipo_usuario = request.form["tipo_usuario"]
        #tipo_usuario = "Proponente"
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
        cur.execute("SELECT * FROM USUARIO WHERE correo_electronico=%s", (correo_electronico, ))

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
            session['nombre'] = nombre
            session['tipo_usuario'] = tipo_usuario

            return redirect(url_for('index')) #Retorna a pagina principal
    
    #En caso que no haya enviado una petición POST verificamos si ya existe una sesión
    if 'correo' in session:
        #Cargar pagina principal
        return redirect(url_for('index'))

    else: #Si no hay sesión activa  
        return render_template("register.html")

#Registrar nuevo proyecto -------------------------------------------------------------------------------------------------------------------------
@app.route('/registerProject', methods=['GET', 'POST'])
def registerProject():

    #Variable de session del usuario
    
    username = session['correo']
    nombre = session['nombre']

    #Si se envia una peticion POST con nuevo proyecto
    if request.method == 'POST':
        # #Comprobacion json completo
        # if not request.json:
        #     return jsonify(
        #         StatusCode = 201,
        #         message="Se requiere enviar un Json por favor"
        #     ), 201
        # # empty_data = False
        # for key in request.json:
        #     if key == '':
        #         # empty_data = True
        #         return jsonify(
        #             StatusCode = 201,
        #             message="No se completaron todos los campos"
        #         ), 201

        nombre_proyecto = request.form["nombre_proyecto"]
        descripcion = request.form["descripcion"]
        justificacion = request.form["justificacion"]
        objetivos = request.form["objetivos"]
        #impacto = request.form["impacto"]
        impacto = "Alto"
        alineacion_ods = request.form["alineacion_ods"] 
        
        # fecha_creacion = request.form["fecha_creacion"]
        now = datetime.now()
        fecha_creacion = now.strftime('%Y-%m-%d %H:%M:%S')

        #Esta funcion me suma la fecha actual y cantidad de meses para conocer la fecha de culminacion de proyecto
        duracion = int(request.form["duracion"])
        fecha_finalizacion = datetime.today() + relativedelta(months=duracion) 

        estado = "Activo"
        tipo_proyecto = request.form["tipo_proyecto"]
        url_video = request.form["url_video"]
        url_imagen = request.form["url_imagen"]
        ciudad = request.form["ciudad"]
        donacion_requerida = request.form["donacion_requerida"]
        perfil_colaborador = request.form["perfil_colaborador"]
        #recursos = request.form["recursos"]  #Revisar
        # correo_creador = request.form["correo_creador"]

        # Create Cursor
        cur= mysql.connection.cursor()

        #Comprobación si existe algun proyecto con el mismo nombre
        cur.execute("SELECT * FROM PROYECTO WHERE nombre_proyecto=%s", (nombre_proyecto, ))

        #¿Existe un proyecto con el mismo nombre?
        if cur.rowcount != 0: # Si
            cur.close() # Close connection
            return jsonify(
                StatusCode = 201,
                message="Ya existe un proyecto con este nombre"
            ), 201

        else: # No
            # Execute Query
            cur.execute("INSERT INTO PROYECTO(nombre_proyecto, descripcion, justificacion, objetivos, impacto, alineacion_ods, fecha_creacion, fecha_finalizacion, estado, tipo_proyecto, url_video, url_imagen, ciudad, donacion_requerida, perfil_colaborador, correo_electronico) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                    (nombre_proyecto, descripcion, justificacion, objetivos, impacto, alineacion_ods, fecha_creacion, fecha_finalizacion, estado, tipo_proyecto, url_video, url_imagen, ciudad, donacion_requerida, perfil_colaborador, username))
            
            # Commit toDB 
            mysql.connection.commit()
                        
            # Close connection
            cur.close()

            # return jsonify(
            #     StatusCode = 201,
            #     message="noError",
            #     data = cur.lastrowid
            # ), 201

            return render_template("Mis_Proyectos.html")
    
    return render_template("Project.html", data = session['nombre'])

    
#Editar información personal -------------------------------------------------------------------------------------------------------------------------
@app.route('/informacion-personal',methods=['GET','POST'])
def informacion_personal():

          
    #En el caso que sea metodo PUT
    if request.method == 'POST':

        # #Comprobacion json completo
        # if not request.json:
        #     return jsonify(
        #         StatusCode = 201,
        #         message="Se requiere enviar un Json por favor"
        #     ), 201

        # # empty_data = False
        # for key in request.json:
        #     if key == '':
        #         # empty_data = True
        #         return jsonify(
        #             StatusCode = 201,
        #             message="No se completaron todos los campos"
        #         ), 201

        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        identificacion = request.form['identificacion']
        ciudad = request.form['ciudad']
        correo = request.form['correo_electronico']
        direccion_residencia = request.form['direccion_residencia']
        sexo = request.form['sexo']
        nacionalidad = request.form['nacionalidad']
        numero_telefonico = request.form['numero_telefonico']
        ocupacion = request.form['ocupacion']

        # Create Cursor
        cur= mysql.connection.cursor()

        #Query de la información personal del usuario logueado
        cur.execute("update usuario set nombre=%s,apellido=%s,edad=%s,identificacion=%s,ciudad=%s,direccion_residencia=%s,sexo=%s,nacionalidad=%s,numero_telefonico=%s,ocupacion=%s where correo_electronico=%s",
                (nombre,apellido,edad,identificacion,ciudad,direccion_residencia,sexo,nacionalidad,numero_telefonico,ocupacion,correo))

        # Commit toDB 
        mysql.connection.commit()
                        
        # Close connection
        cur.close()

        # return jsonify(
        #         StatusCode = 201,
        #         message="Datos actualizados",
        #     ), 201

        return redirect(url_for('informacion_personal'))
  
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
        data=[{
            'nombre':usuario['nombre'],
            'apellido':usuario['apellido'],
            'edad':usuario['edad'],
            'identificacion':usuario['identificacion'],
            'ciudad': usuario['ciudad'],
            'direccion_residencia' : usuario['direccion_residencia'],
            'sexo' : usuario['sexo'],
            'nacionalidad' : usuario['nacionalidad'],
            'numero_telefonico' : usuario['numero_telefonico'],
            'ocupacion' : usuario['ocupacion']
        }]
    
        return render_template("infoPersona.html", data=usuario) 
        
    else: #No
        return jsonify(
            StatusCode = 201,
            message="No se procesaron los datos",
        ), 201

@app.route('/mis-proyectos',methods=['GET'])
def mis_proyectos():

    # #Variable de session del usuario
    # correo_creador = request.json["correo_creador"]
    
    # # Create Cursor
    # cur= mysql.connection.cursor()

    # #Query de la información personal del usuario logueado
    # #SELECT * FROM green_project_bd.PROYECTO A WHERE A.correo_electronico = 'julian@admin.com';
    # cur.execute("SELECT * FROM green_project_bd.PROYECTO A WHERE A.correo_electronico=%s", (correo_creador, ))

    # #Almacenamos el dato en otra variables
    # proyecto = cur.fetchone()

    # #Cierro la consulta
    # cur.close()

    # #Verificamos si obtuvo datos
    # if(proyecto != None):
             
        # return jsonify(
        #     id = proyecto["id"],
        #     nombre_proyecto = proyecto["nombre_proyecto"],
        #     descripcion = proyecto["descripcion"],
        #     justificacion = proyecto["justificacion"],
        #     objetivos = proyecto["objetivos"],
        #     impacto = proyecto["impacto"],
        #     alineacion_ods = proyecto["alineacion_ods"], 
        #     fecha_creacion = proyecto["fecha_creacion"],
        #     fecha_finalizacion = proyecto["fecha_finalizacion"],
        #     estado = proyecto["estado"],
        #     tipo_proyecto = proyecto["tipo_proyecto"],
        #     url_video = proyecto["url_video"],
        #     url_imagen = proyecto["url_imagen"],
        #     ciudad = proyecto["ciudad"],
        #     donacion_requerida = proyecto["donacion_requerida"],
        #     perfil_colaborador = proyecto["perfil_colaborador"],
        #     #recursos = proyecto["recursos"],  #Revisar
        #     correo_creador = proyecto["correo_electronico"],
        # ), 201 

    if 'correo' in session:
        # Create Cursor
        cur= mysql.connection.cursor()

        #Query de la información personal del usuario logueado
        cur.execute("SELECT * FROM PROYECTO WHERE correo_electronico=%s", (session['correo'], ))

        #Almacenamos el dato en otra variables
        proyectos = cur.fetchall()

        #Cierro la consulta
        cur.close()

        return render_template("Mis_Proyectos.html", data = session['nombre'], data2 = proyectos)
    
    else:
        return redirect(url_for('index'))

    # else: #No
    #     return jsonify(
    #         StatusCode = 201,
    #         message="No hay proyecto",
    #     ), 201

@app.route('/infoproyecto/<int:id>',methods=['GET'])
def infoproyecto(id):

    # Create Cursor
    cur= mysql.connection.cursor()

    #Query de la información personal del usuario logueado
    cur.execute("SELECT * FROM PROYECTO WHERE id=%s", (id,))

    #Almacenamos el dato en otra variables
    info_proyectos = cur.fetchall()
        
    print(info_proyectos)
    #Cierro la consulta
    cur.close()

    return render_template("infoproyecto.html", data=info_proyectos)


@app.route('/forgot_password',methods=['GET'])
def forgot_password():
    if 'correo' in session:
        #Cargar pagina principal
        return redirect(url_for('index'))

    else: #Si no hay sesión activa  
        return render_template("forgot-password.html")

  

@app.errorhandler(404)
def page_not_fount(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)