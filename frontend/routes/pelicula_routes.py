import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from global_config import ContenidosConfig as contConf

pelicula_bp = Blueprint('pelicula', __name__)

@pelicula_bp.route('/crear_pelicula', methods=['GET', 'POST'])
def crear_pelicula():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    # Se obtiene el usuario correspondiente al ID y se comprueba si es admin
    
    # Se llama al bakced de actor_controller para obtener la lista de actores
    # y se envia al formulario de pelicula
    
    if request.method == 'GET':
        return render_template("formulario_pelicula.html")
    
    if request.method == 'POST':
        return render_template("formulario_pelicula.html")
    
    return render_template("formulario_pelicula.html")

@pelicula_bp.route('/lista_peliculas', methods=['GET'])
def obtener_peliculas():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    return render_template("peliculas.html")

@pelicula_bp.route('/pelicula/<pelicula_id>', methods=['GET'])
def pelicula(pelicula_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    return render_template("pelicula.html")

@pelicula_bp.route('/editar_pelicula/<pelicula_id>', methods=['GET', 'POST'])
def editar_pelicula(pelicula_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    if request.method == 'GET':
        return render_template("formulario_pelicula.html")
    
    if request.method == 'POST':
        return render_template("formulario_pelicula.html")
    
    return render_template("formulario_pelicula.html")

@pelicula_bp.route('/eliminar_pelicula/<pelicula_id>', methods=['GET'])
def eliminar_pelicula(pelicula_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    return redirect(url_for('pelicula.lista_peliculas'))