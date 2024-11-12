import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from global_config import ContenidosConfig as contConf
from global_config import UsuariosConfig as userConf

actor_bp = Blueprint('actor', __name__)

@actor_bp.route('/crear_actor', methods=['GET', 'POST'])
def crear_actor():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    # Se obtiene el usuario correspondiente al ID y se comprueba si es admin
    response = requests.get(f"{userConf.USUARIOS_BASE_URL}/usuario/{usuario_id}")
    if response.status_code == 200:
        data = response.json()
        es_admin = data.get('esAdmin')
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        return redirect(url_for('user.login'))
    
    if es_admin:
        if request.method == 'GET':
            
            print("Hola cara de bola")
            return render_template("formulario_actor.html")
        
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            fecha_nacimiento = request.form.get('fecha_nacimiento')
            nacionalidad = request.form.get('nacionalidad')
            biografia = request.form.get('biografia')
            
            # Crear el payload para enviar al microservicio
            actor_data = {
                'nombre': nombre,
                'fecha_nacimiento': fecha_nacimiento,
                'nacionalidad': nacionalidad,
                'biografia': biografia
            }
            
            print(actor_data)
            # Hacer la llamada POST al microservicio de películas
            response = requests.post(
                f"{contConf.CONTENIDOS_BASE_URL}/crear_actor", json=actor_data)
            # Manejar la respuesta del microservicio
            if response.status_code == 200:
                try:
                    data = response.json()
                    flash(data['message'], 'success')
                    return redirect(url_for('pelicula.obtener_peliculas'))
                except requests.exceptions.JSONDecodeError:
                    flash("Error al procesar la respuesta del servidor.", 'danger')
                    return render_template("formulario_actor.html")
            else:
                try:
                    data = response.json()
                    flash(data['message'], 'danger')
                except requests.exceptions.JSONDecodeError:
                    flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')
        
        return render_template("formulario_actor.html")
    else:
        flash("No tienes permisos para crear una película.", 'danger')
        return redirect(url_for('pelicula.obtener_peliculas'))

@actor_bp.route('/editar_actor/<actor_id>', methods=['GET', 'POST'])
def editar_actor(actor_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    # Se obtiene el usuario correspondiente al ID y se comprueba si es admin
    response = requests.get(f"{userConf.USUARIOS_BASE_URL}/usuario/{usuario_id}")
    if response.status_code == 200:
        data = response.json()
        es_admin = data.get('esAdmin')
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        return redirect(url_for('user.login'))
    
    if es_admin:
        if request.method == 'GET':
            # Hacer la llamada GET al microservicio de actores para obtener la información del actor
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/obtener_actor/{actor_id}")
            
            if response.status_code == 200:
                actor = response.json()
                return render_template("formulario_actor.html", actor=actor)
            else:
                try:
                    data = response.json()
                    flash(data['message'], 'danger')
                except requests.exceptions.JSONDecodeError:
                    flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')
                return redirect(url_for('pelicula.obtener_peliculas'))
        
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            fecha_nacimiento = request.form.get('fecha_nacimiento')
            nacionalidad = request.form.get('nacionalidad')
            biografia = request.form.get('biografia')
            
            # Crear el payload para enviar al microservicio
            actor_data = {
                'nombre': nombre,
                'fecha_nacimiento': fecha_nacimiento,
                'nacionalidad': nacionalidad,
                'biografia': biografia
            }
            
            # Hacer la llamada PUT al microservicio de actores
            response = requests.put(
                f"{contConf.CONTENIDOS_BASE_URL}/actualizar_actor/{actor_id}", json=actor_data)
            
            if response.status_code == 200:
                flash("Actor actualizado correctamente.", 'success')
                return redirect(url_for('pelicula.obtener_peliculas'))
            else:
                try:
                    data = response.json()
                    flash(data['message'], 'danger')
                except requests.exceptions.JSONDecodeError:
                    flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')
                return redirect(url_for('pelicula.obtener_peliculas'))

@actor_bp.route('/eliminar_actor/<actor_id>', methods=['GET'])
def eliminar_actor(actor_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    # Se obtiene el usuario correspondiente al ID y se comprueba si es admin
    response = requests.get(f"{userConf.USUARIOS_BASE_URL}/usuario/{usuario_id}")
    if response.status_code == 200:
        data = response.json()
        es_admin = data.get('esAdmin')
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        return redirect(url_for('user.login'))
    
    if es_admin:
        # Hacer la llamada DELETE al microservicio de actores
        response = requests.delete(f"{contConf.CONTENIDOS_BASE_URL}/eliminar_actor/{actor_id}")
        
        if response.status_code == 200:
            flash("Actor eliminado correctamente.", 'success')
            return redirect(url_for('pelicula.obtener_peliculas'))
        else:
            try:
                data = response.json()
                flash(data['message'], 'danger')
            except requests.exceptions.JSONDecodeError:
                flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')
            return redirect(url_for('pelicula.obtener_peliculas'))
