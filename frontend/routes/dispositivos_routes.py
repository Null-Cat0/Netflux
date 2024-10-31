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

    if request.method == 'POST':
        import app 
        user_id = session.get('logged_user_id')
        # Comprobación de que tiene 5 o menos dispositivos
        response = requests.get(
            f"{app.USUARIOS_BASE_URL}/usuario/{user_id}/dispositivos")
        
        
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
            f"{app.USUARIOS_BASE_URL}/usuario/{user_id}/dispositivo", json=data)
        if response.status_code == 200:
            flash("Dispositivo creado con éxito", 'success')
            return redirect(url_for('dispositivos.dispositivos'))
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            return redirect(url_for('perfil.obtener_perfiles'))

@dispositivos_bp.route("/eliminar_dispositivo/<nombre_dispositivo>/<int:dispositivo_id>", methods=['POST'])
def eliminar_dispositivo(nombre_dispositivo, dispositivo_id):
    if request.method == 'POST':
        # Usar el ID de usuario de la sesión
        user_id = session.get('logged_user_id')
        import app
        if user_id is None:
            flash("Error: No se encontró el usuario en la sesión.", 'danger')
            return redirect(url_for('auth.login'))

        url = f"{app.USUARIOS_BASE_URL}/usuario/{user_id}/dispositivo/{nombre_dispositivo}/{dispositivo_id}"
        
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

@dispositivos_bp.route("/editar_dispositivo/<nombre_dispositivo>/<int:dispositivo_id>", methods=['GET', 'POST'])
def editar_dispositivo(nombre_dispositivo, dispositivo_id):
    if request.method == 'GET':
        # Pasar datos al template para pre-rellenar el formulario
        return render_template(
            "crear_dispositivo.html",
            nombre_dispositivo=nombre_dispositivo,
            dispositivo_id=dispositivo_id
        )
    
    if request.method == 'POST':
        import app
        user_id = session.get('logged_user_id')
        if not user_id:
            flash("Error: Usuario no autenticado.", 'danger')
            return redirect(url_for('auth.login'))

        # Construir los datos a enviar en la solicitud PUT
        data = {
            "nombre_dispositivo": request.form['nombre_dispositivo'],
            "tipo_dispositivo": request.form['tipo_dispositivo']
        }
        url = f"{app.USUARIOS_BASE_URL}/usuario/{user_id}/dispositivo/{nombre_dispositivo}/{dispositivo_id}"
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
