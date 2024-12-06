import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime

from config import ContenidosConfig as contConf
from config import UsuariosConfig as userConf

actor_bp = Blueprint('actor', __name__)

@actor_bp.route('/crear_actor', methods=['GET', 'POST'])
def crear_actor():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    
    
    if es_admin:
        if request.method == 'GET':
            
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
            
            # Hacer la llamada POST al microservicio de películas
            response = requests.post(
                f"{contConf.CONTENIDOS_BASE_URL}/actores", json=actor_data)
            # Manejar la respuesta del microservicio
            if response.status_code == 201:
                try:
                    data = response.json()
                    flash(data['message'], 'success')
                    return redirect(url_for('actor.obtener_actores'))
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
    
    es_admin = session.get('es_admin')
    
    
    if es_admin:
        if request.method == 'GET':
            # Hacer la llamada GET al microservicio de actores para obtener la información del actor
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/actores/{actor_id}")
            
            if response.status_code == 200:
                actor = response.json()
                actor["fecha_nacimiento"] = datetime.strptime(actor["fecha_nacimiento"], '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%d-%m')
                return render_template("formulario_actor.html", actor=actor)
            else:
                try:
                    data = response.json()
                    flash(data['message'], 'danger')
                except requests.exceptions.JSONDecodeError:
                    flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')
                return redirect(url_for('pelicula.obtener_actores'))
        
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
                f"{contConf.CONTENIDOS_BASE_URL}/actores/{actor_id}", json=actor_data)
            
            if response.status_code == 200:
                flash("Actor actualizado correctamente.", 'success')
                return redirect(url_for('actor.obtener_actores'))
            else:
                try:
                    data = response.json()
                    flash(data['message'], 'danger')
                except requests.exceptions.JSONDecodeError:
                    flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')
                return redirect(url_for('actor.obtener_actores'))

@actor_bp.route('/eliminar_actor/<actor_id>', methods=['GET'])
def eliminar_actor(actor_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    
    if es_admin:
        # Hacer la llamada DELETE al microservicio de actores
        response = requests.delete(f"{contConf.CONTENIDOS_BASE_URL}/actores/{actor_id}")
        
        if response.status_code == 200:
            flash("Actor eliminado correctamente.", 'success')
            return redirect(url_for('actor.obtener_actores'))
        else:
            try:
                data = response.json()
                flash(data['message'], 'danger')
            except requests.exceptions.JSONDecodeError:
                flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')
            return redirect(url_for('actor.obtener_actores'))

@actor_bp.route('/lista_actores', methods=['GET'])
def obtener_actores():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    
    # Se llama al microservicio de actores para obtener la lista de actores
    response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/actores")
    if response.status_code == 200:
        actores = response.json()
        for actor in actores:
            actor['fecha_nacimiento'] = datetime.strptime(actor["fecha_nacimiento"], '%a, %d %b %Y %H:%M:%S %Z').strftime('%d/%m/%Y')
        return render_template("actores.html", actores=actores, es_admin=es_admin)
    else:
        try:
            data = response.json()
            flash(data['message'], 'danger')
        except requests.exceptions.JSONDecodeError:
            flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')
        return render_template("actores.html", actores=[])
    
    