import requests
from flask import render_template, request, redirect, url_for, flash, session, Blueprint

from config import UsuariosConfig as userConf

usuario_bp = Blueprint('user', __name__)

@usuario_bp.route('/iniciar_sesion', methods=['GET', 'POST'])
def login():
    if session.get('logged_user_id'):
        flash("Ya has iniciado sesión.", 'info')
        return redirect(url_for('perfil.obtener_perfiles'))
    
    if request.method == 'GET':
        return render_template("inicio_sesion.html")

    if request.method == 'POST':
        # Capturar datos del formulario
        correo_electronico = request.form.get('correo')
        password = request.form.get('password')

        # Crear el payload para enviar al microservicio
        login_data = {
            'correo_electronico': correo_electronico,
            'password': password
        }
        # Hacer la llamada POST al microservicio de autenticación
        response = requests.post(
            f"{userConf.USUARIOS_BASE_URL}/iniciar_sesion", json=login_data)

        # Manejar la respuesta del microservicio
        if response.status_code == 200:
            try:
                data = response.json()
                flash(data['message'], 'success')
                # Almacenar datos en la sesión
                session.permanent = True
                session['logged_user_id'] = data['usuario']['user_id']
                session['logged_user_name'] = data['usuario']['nombre']
                session['es_admin'] = data['usuario']['esAdmin']

                # Redirigir al perfil del usuario
                return redirect(url_for('perfil.obtener_perfiles'))
            except requests.exceptions.JSONDecodeError:
                flash("Error al procesar la respuesta del servidor.", 'danger')
                return render_template("inicio_sesion.html")
        else:
            try:
                data = response.json()
                flash(data['message'], 'danger')
            except requests.exceptions.JSONDecodeError:
                flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')

    return render_template("inicio_sesion.html")

@usuario_bp.route('/cerrar_sesion')
def cerrar_sesion():
    # Elimina 'logged_user_id' de la sesión para cerrar sesión
    # session.pop('logged_user_id', None)
    # session.pop('logged_user_id', None)
    # session.pop('perfil_id', None)
    session.clear()
    # Mensaje opcional para el usuario
    flash("Has cerrado sesión con éxito.", "info")
    # Redirige a la página de inicio de sesión o a la página principal
    return redirect(url_for('user.login'))

@usuario_bp.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'GET':
        # Renderiza el formulario de creación de cuenta
        return render_template("formulario_usuario.html")

    if request.method == 'POST':
        dispositivos = []
        # Capturar datos del formulario
        nombre = request.form.get('nombre')
        correo_electronico = request.form.get('correo_electronico')
        password = request.form.get('password')
        pais = request.form.get('pais')
        plan_suscripcion = request.form.get('plan_suscripcion')
        dispositivos.append(request.form.get('dispositivos'))
        esAdmin = request.form.get('admin')

        # Crear el payload para enviar al microservicio
        usuario_data = {
            'nombre': nombre,
            'correo_electronico': correo_electronico,
            'password': password,
            'pais': pais,
            'plan_suscripcion': plan_suscripcion,
            'dispositivos': dispositivos,
            'esAdmin': esAdmin
        }

        # Hacer la solicitud POST al microservicio para crear el usuario
        response = requests.post(
            f"{userConf.USUARIOS_BASE_URL}/usuarios", json=usuario_data)

        # Manejar la respuesta del microservicio
        if response.status_code == 201:
            flash('Usuario creado con éxito', 'success')
            return redirect(url_for('user.login'))
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')

    return render_template("formulario_usuario.html")

@usuario_bp.route('/cuenta', methods=['GET', 'POST'])
def editar_usuario():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Debes iniciar sesión para acceder a esta página", 'danger')
        return redirect(url_for('user.login'))

    if request.method == 'GET':
        response = requests.get(
            f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}"
        )
        if response.status_code == 200:
            data = response.json()
            return render_template("formulario_usuario.html", cuenta=data)
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            # Redirigir a una vista de error si es necesario
            return redirect(url_for('user.login'))

    if request.method == 'POST':
        dispositivos = []
        # Capturar datos del formulario
        nombre = request.form.get('nombre')
        correo_electronico = request.form.get('correo_electronico')
        pais = request.form.get('pais')
        plan_suscripcion = request.form.get('plan_suscripcion')
        dispositivos.append(request.form.get('dispositivos'))
        esAdmin = request.form.get('admin')

        # Verificación de campos obligatorios
        if not nombre or not correo_electronico:
            flash("Todos los campos son obligatorios.", 'danger')
            # Redirigir a la misma página para corregir
            return redirect(url_for('user.editar_usuario'))

        # Crear el payload para enviar al microservicio
        usuario_data = {
            'nombre': nombre,
            'correo_electronico': correo_electronico,
            'pais': pais,
            'plan_suscripcion': plan_suscripcion,
            'dispositivos': dispositivos,
            'esAdmin': esAdmin
        }
        # Hacer la solicitud PUT al microservicio para actualizar el usuario
        response = requests.put(
            f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}", json=usuario_data)

        if response.status_code == 200:
            session['logged_user_name'] = nombre
            flash("Usuario actualizado con éxito", 'success')

            # Actualizar la sesión con el valor booleano correcto
            es_admin_bool = esAdmin == '1'
            session['es_admin'] = es_admin_bool

            # Redirigir a la vista de perfiles
            return redirect(url_for('perfil.obtener_perfiles'))
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            # Redirigir a la misma página para corregir
            return redirect(url_for('user.editar_usuario'))


@usuario_bp.route('/actualizar_password', methods=['GET', 'POST'])
def actualizar_password():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Debes iniciar sesión para acceder a esta página", 'danger')
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        # Capturar datos del formulario
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        # Crear el payload para enviar al microservicio
        password_data = {
            'old_password': old_password,
            'new_password': new_password
        }

        # Hacer la solicitud PATCH al microservicio para actualizar la contraseña
        response = requests.patch(
            f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}/password", json=password_data)

        if response.status_code == 200:
            flash("Contraseña actualizada con éxito", 'success')
            return redirect(url_for('perfil.obtener_perfiles'))
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            return redirect(url_for('user.actualizar_password'))
    
    return render_template('actualizar_password.html')


@usuario_bp.route('/borrar_cuenta')
def borrar_cuenta():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Debes iniciar sesión para acceder a esta página", 'danger')
        return redirect(url_for('user.login'))

    response = requests.delete(
        f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}")

    if response.status_code == 200:
        flash("Cuenta eliminada con éxito", 'success')
        return redirect(url_for('user.cerrar_sesion'))
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        return redirect(url_for('user.login'))
    
