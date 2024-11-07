import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from global_config import ContenidosConfig as contConf

serie_bp = Blueprint('serie', __name__)

@serie_bp.route('/crear_serie', methods=['GET', 'POST'])

##########################################################
# HAY QUE VER SI LO DE TEMPORADA Y CAPITULO SE HACE AQUI #
##########################################################

def crear_serie():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    # Se obtiene el usuario correspondiente al ID y se comprueba si es admin
    
    # Se llama al bakced de actor_controller para obtener la lista de actores
    # y se envia al formulario de serie
    
    if request.method == 'GET':
        return render_template("formulario_serie.html")
    
    if request.method == 'POST':
        return render_template("formulario_serie.html")
    
    return render_template("formulario_serie.html")

@serie_bp.route('/lista_series', methods=['GET'])
def obtener_series():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    return render_template("lista_series.html")

@serie_bp.route('/serie/<serie_id>', methods=['GET'])
def serie(serie_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    return render_template("serie.html")

@serie_bp.route('/editar_serie/<serie_id>', methods=['GET', 'POST'])
def editar_serie(serie_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    if request.method == 'GET':
        return render_template("formulario_serie.html")
    
    if request.method == 'POST':
        return render_template("formulario_serie.html")
    
    return render_template("formulario_serie.html")

@serie_bp.route('/eliminar_serie/<serie_id>', methods=['GET'])
def eliminar_serie(serie_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    return redirect(url_for('serie.listar_series'))

@serie_bp.route('/crear_temporada', methods=['GET', 'POST'])
def crear_temporada():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    # Se obtiene el usuario correspondiente al ID y se comprueba si es admin
    
    if request.method == 'GET':
        return render_template("formulario_temporada.html")
    
    if request.method == 'POST':
        return render_template("formulario_temporada.html")
    
    return render_template("formulario_temporada.html")

@serie_bp.route('/editar_temporada/<temporada_id>', methods=['GET', 'POST'])
def editar_temporada(temporada_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    if request.method == 'GET':
        return render_template("formulario_temporada.html")
    
    if request.method == 'POST':
        return render_template("formulario_temporada.html")
    
    return render_template("formulario_temporada.html")

@serie_bp.route('/eliminar_temporada/<temporada_id>', methods=['GET'])
def eliminar_temporada(temporada_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    return redirect(url_for('serie.listar_temporadas'))

@serie_bp.route('/crear_capitulo', methods=['GET', 'POST'])
def crear_capitulo():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    # Se obtiene el usuario correspondiente al ID y se comprueba si es admin
    
    if request.method == 'GET':
        return render_template("formulario_capitulo.html")
    
    if request.method == 'POST':
        return render_template("formulario_capitulo.html")
    
    return render_template("formulario_capitulo.html")

@serie_bp.route('/editar_capitulo/<capitulo_id>', methods=['GET', 'POST'])
def editar_capitulo(capitulo_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    if request.method == 'GET':
        return render_template("formulario_capitulo.html")
    
    if request.method == 'POST':
        return render_template("formulario_capitulo.html")
    
    return render_template("formulario_capitulo.html")

@serie_bp.route('/eliminar_capitulo/<capitulo_id>', methods=['GET'])
def eliminar_capitulo(capitulo_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    return redirect(url_for('serie.listar_capitulos'))