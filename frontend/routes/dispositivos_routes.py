import requests
from flask import Blueprint, request, render_template, flash, redirect, url_for, session

from global_config import UsuariosConfig as userConf

dispositivos_bp = Blueprint('dispositivos', __name__)

@dispositivos_bp.route("/dispositivos", methods=['GET', 'POST'])
def dispositivos():
    if request.method == 'GET':
        user_id = session.get('logged_user_id')
        if not user_id:
            flash("Usuario no autenticado.", 'danger')
            return redirect(url_for('user.login'))
        response = requests.get(
            f"{userConf.USUARIOS_BASE_URL}/usuarios/{user_id}/dispositivos")
        if response.status_code == 200:
            data = response.json()
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
        return render_template("formulario_dispositivo.html")

    if request.method == 'POST':
        user_id = session.get('logged_user_id')
        # Comprobación de que tiene 5 o menos dispositivos
        response = requests.get(
            f"{userConf.USUARIOS_BASE_URL}/usuarios/{user_id}/dispositivos")
        
        if response.status_code == 200:
            data = response.json()
            if len(data) >= 5:
                flash("No puedes tener más de 5 dispositivos", 'danger')
                return redirect(url_for('dispositivos.dispositivos'))
        else:   
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            return redirect(url_for('perfil.obtener_perfiles'))         
        
        data = {
            "nombre_dispositivo": request.form['nombre_dispositivo'],
            "tipo_dispositivo": request.form['tipo_dispositivo']
        }
        response = requests.post(
            f"{userConf.USUARIOS_BASE_URL}/usuarios/{user_id}/dispositivos", json=data)
        if response.status_code == 200:
            flash("Dispositivo creado con éxito", 'success')
            return redirect(url_for('dispositivos.dispositivos'))
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            return redirect(url_for('dispositivos.dispositivos'))

@dispositivos_bp.route("/eliminar_dispositivo/<nombre_dispositivo>/<dispositivo_id>", methods=['POST'])
def eliminar_dispositivo(nombre_dispositivo, dispositivo_id):
    if request.method == 'POST':
        # Usar el ID de usuario de la sesión
        user_id = session.get('logged_user_id')
        if user_id is None:
            flash("Error: No se encontró el usuario en la sesión.", 'danger')
            return redirect(url_for('auth.login'))

        url = f"{userConf.USUARIOS_BASE_URL}/usuarios/{user_id}/dispositivos/{dispositivo_id}/{nombre_dispositivo}"
        
        # Realizar la solicitud DELETE
        response = requests.delete(url)

        # Verificar la respuesta de la solicitud
        if response.status_code == 200:
            flash("Dispositivo eliminado con éxito", 'success')
            return redirect(url_for('dispositivos.dispositivos'))
        else:
            # Intentar obtener el mensaje de error solo si la respuesta tiene JSON
            try:
                error_message = response.json().get('message', 'Error desconocido')
            except requests.JSONDecodeError:
                error_message = 'Error desconocido: no se pudo decodificar la respuesta del servidor.'

            flash(f"Error al eliminar el dispositivo: {error_message}", 'danger')
            return redirect(url_for('dispositivos.dispositivos'))

@dispositivos_bp.route("/editar_dispositivo/<nombre_dispositivo>/<dispositivo_id>", methods=['GET', 'POST'])
def editar_dispositivo(nombre_dispositivo, dispositivo_id):
    if request.method == 'GET':
        # Pasar datos al template para pre-rellenar el formulario
        return render_template(
            "formulario_dispositivo.html",
            nombre_dispositivo=nombre_dispositivo,
            dispositivo_id=dispositivo_id
        )
    
    if request.method == 'POST':
        user_id = session.get('logged_user_id')

        # Asegurarse de capturar los valores del formulario correctamente
        nombre_dispositivo_actualizado = request.form.get('nombre_dispositivo')
        tipo_dispositivo_actualizado = request.form.get('tipo_dispositivo')

        print(f"\nNombre dispositivo: {nombre_dispositivo_actualizado}\n")
        print(f"\nDispositivo ID: {tipo_dispositivo_actualizado}\n")
        
        if not nombre_dispositivo_actualizado or not tipo_dispositivo_actualizado:
            flash("Error: Los campos del formulario están vacíos.", 'danger')
            return redirect(url_for('dispositivos.editar_dispositivo', nombre_dispositivo=nombre_dispositivo, dispositivo_id=dispositivo_id))

        data = {
            "nombre_dispositivo": nombre_dispositivo_actualizado,
            "dispositivo_id": tipo_dispositivo_actualizado
        }

        url = f"{userConf.USUARIOS_BASE_URL}/usuarios/{user_id}/dispositivos/{dispositivo_id}/{nombre_dispositivo}"
        response = requests.put(url, json=data)
        
        if response.status_code == 200:
            flash("Dispositivo actualizado con éxito", 'success')
            return redirect(url_for('dispositivos.dispositivos'))
        else:
            try:
                error_message = response.json().get('message', 'Error desconocido')
            except requests.JSONDecodeError:
                error_message = 'Error desconocido al actualizar el dispositivo.'
            flash(f"Error: {error_message}", 'danger')
            return redirect(url_for('dispositivos.dispositivos'))