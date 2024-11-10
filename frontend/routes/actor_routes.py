import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from global_config import ContenidosConfig as contConf

actor_bp = Blueprint('actor', __name__)

@actor_bp.route('/crear_actor', methods=['GET', 'POST'])
def crear_actor():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    # Se obtiene el usuario correspondiente al ID y se comprueba si es admin
    
    if request.method == 'GET':
        return render_template("formulario_actor.html")
    
    if request.method == 'POST':
        return render_template("formulario_actor.html")
    
    return render_template("formulario_actor.html")

@actor_bp.route('/editar_actor/<actor_id>', methods=['GET', 'POST'])
def editar_actor(actor_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    # Se obtiene el usuario correspondiente al ID y se comprueba si es admin
    
    if request.method == 'GET':
        return render_template("formulario_actor.html")
    
    if request.method == 'POST':
        return render_template("formulario_actor.html")
    
    return render_template("formulario_actor.html")

@actor_bp.route('/eliminar_actor/<actor_id>', methods=['GET'])
def eliminar_actor(actor_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    return redirect(url_for('actor.listar_actores'))