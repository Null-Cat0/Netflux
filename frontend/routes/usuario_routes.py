import requests
from flask import render_template, request, redirect, url_for, flash, session, Blueprint

from global_config import UsuariosConfig as userConf

usuario_bp = Blueprint('user', __name__)

@usuario_bp.route('/iniciar_sesion', methods=['GET', 'POST'])
def login():
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
    session.pop('logged_user_id', None)
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

        # Crear el payload para enviar al microservicio
        usuario_data = {
            'nombre': nombre,
            'correo_electronico': correo_electronico,
            'password': password,
            'pais': pais,
            'plan_suscripcion': plan_suscripcion,
            'dispositivos': dispositivos
        }

        # Hacer la solicitud POST al microservicio para crear el usuario
        response = requests.post(
            f"{userConf.USUARIOS_BASE_URL}/crear_usuario", json=usuario_data)

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
    perfil_id = request.args.get('perfil_id', default='')
    usuario_id = session.get('logged_user_id')

    if request.method == 'GET':
        response = requests.get(
            f"{userConf.USUARIOS_BASE_URL}/usuario/{usuario_id}"
        )
        if response.status_code == 200:
            data = response.json()
            return render_template("formulario_usuario.html", cuenta=data)
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            # Redirigir a una vista de error si es necesario
            return redirect(url_for('some_error_handling_view'))

    if request.method == 'POST':
        dispositivos = []
        # Capturar datos del formulario
        nombre = request.form.get('nombre')
        correo_electronico = request.form.get('correo_electronico')
        password = request.form.get('password')
        pais = request.form.get('pais')
        plan_suscripcion = request.form.get('plan_suscripcion')
        dispositivos.append(request.form.get('dispositivos'))

        # Verificación de campos obligatorios
        if not nombre or not correo_electronico or not password:
            flash("Todos los campos son obligatorios.", 'danger')
            # Redirigir a la misma página para corregir
            return redirect(url_for('editar_usuario'))

        # Crear el payload para enviar al microservicio
        usuario_data = {
            'nombre': nombre,
            'correo_electronico': correo_electronico,
            'password': password,
            'pais': pais,
            'plan_suscripcion': plan_suscripcion,
            'dispositivos': dispositivos
        }

        # Hacer la solicitud PUT al microservicio para actualizar el usuario
        response = requests.put(
            f"{userConf.USUARIOS_BASE_URL}/actualizar_usuario/{usuario_id}", json=usuario_data)

        if response.status_code == 200:
            session['logged_user_name'] = nombre
            flash("Usuario actualizado con éxito", 'success')
            # Redirigir a la vista de perfiles
            return redirect(url_for('perfil.obtener_perfiles'))
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            # Redirigir a la misma página para corregir
            return redirect(url_for('editar_usuario'))

    # Si no se maneja el método, retornar a la página de cuenta o un error
    # Cambia esto según sea necesario
    return redirect(url_for('some_default_view'))

@usuario_bp.route('/borrar_cuenta')
def borrar_cuenta():
    usuario_id = session.get('logged_user_id')

    response = requests.delete(
        f"{userConf.USUARIOS_BASE_URL}/eliminar_usuario/{usuario_id}")

    if response.status_code == 200:
        flash("Cuenta eliminada con éxito", 'success')
        return redirect(url_for('user.cerrar_sesion'))
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        return redirect(url_for('user.login'))
