import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from global_config import ContenidosConfig as contConf
from global_config import UsuariosConfig as userConf
from global_config import VisualizacionesConfig

pelicula_bp = Blueprint('pelicula', __name__)

@pelicula_bp.route('/crear_pelicula', methods=['GET', 'POST'])
def crear_pelicula():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    

    # Se llama al bakced de actor_controller para obtener la lista de actores
    # y se envia al formulario de pelicula
        # Obtener el usuario correspondiente al ID y comprobar si es admin
    es_admin = session.get('es_admin')
    
    if es_admin:
        if request.method == 'GET':
            # Obtener todos los generos
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/listar_generos")
            if response.status_code == 200:
                generos = response.json()
            
            # Obtener todos los actores
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/listar_actores")
            if response.status_code == 200:
                actores = response.json()
            
            return render_template("formulario_pelicula.html", generos=generos, actores=actores, es_admin=es_admin, pelicula={})
        
        if request.method == 'POST':
            # Otros datos del formulario
            titulo = request.form.get('titulo')
            sinopsis = request.form.get('sinopsis')
            genero = request.form.getlist('generos')
            anio_estreno = request.form.get('anio_estreno')
            duracion = request.form.get('duracion')
            
            # Obtener los IDs de actores seleccionados
            actores = request.form.getlist('actores')
            
            pelicula_data = {
                'titulo': titulo,
                'sinopsis': sinopsis,
                'genero': genero,
                'anio_estreno': anio_estreno,
                'duracion': duracion,
                'actores': actores,  # Lista de IDs de actores seleccionados
            }
            
            # Realizar la llamada POST al microservicio o procesar la información


            response = requests.post(
                f"{contConf.CONTENIDOS_BASE_URL}/crear_pelicula", json=pelicula_data)
            
            # Manejar la respuesta del microservicio
            if response.status_code == 201:
                try:
                    data = response.json()
                    flash(data['message'], 'success')
                    return redirect(url_for('pelicula.obtener_peliculas'))
                except requests.exceptions.JSONDecodeError:
                    flash("Error al procesar la respuesta del servidor.", 'danger')
                    return render_template("formulario_pelicula.html")
            else:
                try:
                    data = response.json()
                    flash(data['message'], 'danger')
                except requests.exceptions.JSONDecodeError:
                    flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')
                    return render_template("formulario_pelicula.html")
                        
            return redirect(url_for('pelicula.obtener_peliculas'))
    else:
        flash("No tienes permisos para crear una película.", 'danger')
        return redirect(url_for('pelicula.obtener_peliculas'))
    
@pelicula_bp.route('/lista_peliculas', methods=['GET'])
def obtener_peliculas():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))

    es_admin = session.get('es_admin')
    
    # Se realiza la solicitud GET al microservicio de contenidos para obtener la lista de películas
    response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/listar_peliculas")
    print("El codigo es:", response.status_code)
    if response.status_code == 200:
        data = response.json()
        return render_template("peliculas.html", es_admin=es_admin, peliculas=data)
    else:
        data = response.json()
        flash(f"Error al obtener las películas: {data['message']}", 'danger')        
    
    return render_template("peliculas.html", es_admin=es_admin, peliculas=[])

@pelicula_bp.route('/pelicula/<pelicula_id>', methods=['GET'])
def pelicula(pelicula_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    # Hacer la solicitud GET al microservicio de contenidos para obtener la información de la película
    response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/obtener_pelicula/{pelicula_id}")
    if response.status_code == 200:
        data = response.json()
        return render_template("pelicula.html", pelicula=data)
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
    
    return render_template("pelicula.html", pelicula={})

@pelicula_bp.route('/editar_pelicula/<pelicula_id>', methods=['GET', 'POST'])
def editar_pelicula(pelicula_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    
    if es_admin:
        if request.method == 'GET':
            # Hacer la llamada GET al microservicio de películas para obtener la información de la película
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/obtener_pelicula/{pelicula_id}")
            
            if response.status_code == 200:
                pelicula = response.json()
                # Obtener todos los generos
                response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/listar_generos")
                if response.status_code == 200:
                    data = response.json()
                    genero_nombre_id = []  # Crear una lista para almacenar los generos como diccionarios
                    for genero in data:
                        genero_nombre_id.append({
                            'id': genero.get('id', 'N/A'),  
                            'nombre': genero.get('nombre', 'N/A')  
                        })
                # Obtener todos los actores
                response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/listar_actores")
                if response.status_code == 200:
                    data = response.json()
                    actor_nombre_id = []  # Crear una lista para almacenar los actores como diccionarios
                    for actor in data:
                        actor_nombre_id.append({
                            'id': actor.get('id', 'N/A'),  
                            'nombre': actor.get('nombre', 'N/A')  
                        })

                return render_template("formulario_pelicula.html", generos=genero_nombre_id, actores=actor_nombre_id, pelicula=pelicula, es_admin=es_admin)
            else:
                try:
                    data = response.json()
                    flash(data['message'], 'danger')
                except requests.exceptions.JSONDecodeError:
                    flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')
                return redirect(url_for('pelicula.obtener_peliculas'))
        if request.method == 'POST':
            titulo = request.form.get('titulo')
            sinopsis = request.form.get('sinopsis')
            genero = request.form.getlist('generos')
            anio_estreno = request.form.get('anio_estreno')
            duracion = request.form.get('duracion')
            actores = request.form.getlist('actores')


            print(actores)
            if actores is None: 
                actores = []    
            # Crear el payload para enviar al microservicio
            pelicula_data = {
                'titulo': titulo,
                'sinopsis': sinopsis,
                'genero': genero,
                'anio_estreno': anio_estreno,
                'duracion': duracion,
                'actores': actores if actores else [],  # Lista de IDs de actores seleccionados
            }
            # Hacer la llamada PUT al microservicio de películas
            response = requests.put(
                f"{contConf.CONTENIDOS_BASE_URL}/editar_pelicula/{pelicula_id}", json=pelicula_data)
            # Manejar la respuesta del microservicio
            if response.status_code == 200:
                try:
                    data = response.json()
                    flash(data['message'], 'success')
                    return redirect(url_for('pelicula.obtener_peliculas'))
                except requests.exceptions.JSONDecodeError:
                    flash("Error al procesar la respuesta del servidor.", 'danger')
                    return render_template("formulario_pelicula.html")
            else:
                try:
                    data = response.json()
                    flash(data['message'], 'danger')
                except requests.exceptions.JSONDecodeError:
                    flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')

@pelicula_bp.route('/eliminar_pelicula/<pelicula_id>', methods=['GET'])
def eliminar_pelicula(pelicula_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    es_admin = session.get('es_admin')

    if es_admin:
        # Antes de borrar la película, se debe verificar si la película está en:
        # - En la lista de reproducción (mi lista del perfil)
        # - Alguna recomendación
        # - Alguna visualización y por ello, en el historial

        ## Primero se obtienen los usuarios
        response = requests.get(f"{userConf.USUARIOS_BASE_URL}/listar_usuarios")
        if response.status_code != 200:
            flash("Error al obtener la lista de usuarios.", 'danger')
            return redirect(url_for('pelicula.obtener_peliculas'))
        usuarios = response.json()

        ## Luego se obtienen los perfiles de cada usuario
        perfiles = []
        for usuario in usuarios:
            response = requests.get(f"{userConf.USUARIOS_BASE_URL}/usuario/{usuario['user_id']}/perfiles")
            if response.status_code != 200:
                flash(f"Error al obtener los perfiles del usuario {usuario['user_id']}.", 'danger')
                return redirect(url_for('pelicula.obtener_peliculas'))
            perfiles += response.json()

        ## Se borran las visualizaciones de la película para cada perfil
        for perfil in perfiles:
            user_id = perfil["user_id"]
            perfil_id = perfil["perfil_id"]

            response = requests.delete(f"{VisualizacionesConfig.VISUALIZACIONES_BASE_URL}/usuario/{user_id}/perfil/{perfil_id}/visualizacion/{pelicula_id}")
            if response.status_code not in [200, 404]:
                flash(f"Error al eliminar las visualizaciones del perfil {perfil_id}.", 'danger')
                return redirect(url_for('pelicula.obtener_peliculas'))

            # Tras verificar el historial, se verifican las listas de recomendaciones
            response = requests.get(f"{VisualizacionesConfig.VISUALIZACIONES_BASE_URL}/usuario/{user_id}/perfil/{perfil_id}/recomendacion")
            if response.status_code != 200:
                flash(f"Error al obtener las recomendaciones del perfil {perfil_id}.", 'danger')
                return redirect(url_for('pelicula.obtener_peliculas'))
            recomendaciones = response.json()

            lista_peliculas = recomendaciones['peliculas']
            if pelicula_id in lista_peliculas:
                lista_peliculas.remove(pelicula_id)
                response = requests.patch(f"{VisualizacionesConfig.VISUALIZACIONES_BASE_URL}/usuario/{user_id}/perfil/{perfil_id}/recomendacion", json={'peliculas_recomendadas': lista_peliculas})
                if response.status_code != 200:
                    flash(f"Error al eliminar la película {pelicula_id} de las recomendaciones del perfil {perfil_id}.", 'danger')
                    return redirect(url_for('pelicula.obtener_peliculas'))

            # Se borra el contenido de la lista del perfil
            response = requests.delete(f"{userConf.USUARIOS_BASE_URL}/usuario/{user_id}/perfiles/{perfil_id}/lista/{pelicula_id}")
            if response.status_code not in [200, 404]: # 404 si no existe la lista
                flash(f"Error al eliminar la película {pelicula_id} de la lista del perfil {perfil_id}.", 'danger')
                return redirect(url_for('pelicula.obtener_peliculas'))

        # Hacer la solicitud DELETE al microservicio para eliminar la película
        response = requests.delete(f"{contConf.CONTENIDOS_BASE_URL}/eliminar_pelicula/{pelicula_id}")
        if response.status_code == 200:
            flash("Película eliminada con éxito.", 'success')
        else:
            data = response.json()
            flash(f"Error al eliminar la película: {data['message']}", 'danger')
        return redirect(url_for('pelicula.obtener_peliculas'))

    return redirect(url_for('pelicula.lista_peliculas'))