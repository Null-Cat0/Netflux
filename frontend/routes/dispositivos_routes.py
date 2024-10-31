import requests
from flask import Blueprint, request, render_template, flash, redirect, url_for, session

dispositivos_bp = Blueprint('dispositivos', __name__)

@dispositivos_bp.route("/dispositivos", methods=['GET', 'POST'])
def dispositivos():
    import app
    if request.method == 'GET':
        user_id = session.get('logged_user_id')
        if not user_id:
            flash("Usuario no autenticado.", 'danger')
            return redirect(url_for('user.login'))
        response = requests.get(
            f"{app.USUARIOS_BASE_URL}/usuario/{user_id}/dispositivos")
        if response.status_code == 200:
            data = response.json()
            print (data)
            return render_template("dispositivos.html", dispositivos=data)
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            return redirect(url_for('perfil.obtener_perfiles'))
    
@dispositivos_bp.route("/crear_dispositivo", methods=['GET', 'POST'])
def crear_dispositivo():
    if request.method == 'GET':
        user_id = session.get('logged_user_id')
        if not user_id:
            flash("Usuario no autenticado.", 'danger')
            return redirect(url_for('user.login'))
        return render_template("crear_dispositivo.html")
