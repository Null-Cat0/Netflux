import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta

from routes import usuario_controller
from routes import perfil_controller
from routes import dispositivo_controller

app = Flask(__name__)
app.secret_key = 'secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

# Moved
#@app.route('/iniciar_sesion', methods=['GET', 'POST'])
#def login():
#    if request.method == 'GET':
#        return render_template("inicio_sesion.html")
#
#    if request.method == 'POST':
#        # Capturar datos del formulario
#        correo_electronico = request.form.get('correo')
#        password = request.form.get('password')
#
#        # Crear el payload para enviar al microservicio
#        login_data = {
#            'correo_electronico': correo_electronico,
#            'password': password
#        }
#
#        # Hacer la llamada POST al microservicio de autenticación
#        response = requests.post(
#            'http://localhost:8080/iniciar_sesion', json=login_data)
#
#        # Manejar la respuesta del microservicio
#        if response.status_code == 200:
#            try:
#                data = response.json()
#                flash(data['message'], 'success')
#                # Almacenar datos en la sesión
#                session.permanent = True
#                session['logged_user_id'] = data['usuario']['user_id']
#                session['logged_user_name'] = data['usuario']['nombre']
#
#                # Redirigir al perfil del usuario
#                return redirect(url_for('obtener_perfiles'))
#            except requests.exceptions.JSONDecodeError:
#                flash("Error al procesar la respuesta del servidor.", 'danger')
#                return render_template("inicio_sesion.html")
#        else:
#            try:
#                data = response.json()
#                flash(data['message'], 'danger')
#            except requests.exceptions.JSONDecodeError:
#                flash("Error en el servidor. No se recibió una respuesta válida.", 'danger')
#
#    return render_template("inicio_sesion.html")
#
#
# Moved
#@app.route('/cerrar_sesion')
#def cerrar_sesion():
#    # Elimina 'logged_user_id' de la sesión para cerrar sesión
#    session.pop('logged_user_id', None)
#    # Mensaje opcional para el usuario
#    flash("Has cerrado sesión con éxito.", "info")
#    # Redirige a la página de inicio de sesión o a la página principal
#    return redirect(url_for('login'))
#
#
# Moved
#@app.route('/crear_usuario', methods=['GET', 'POST'])
#def crear_usuario():
#    if request.method == 'GET':
#        # Renderiza el formulario de creación de cuenta
#
#        return render_template("crear_usuario.html")
#
#    if request.method == 'POST':
#        dispositivos = []
#        # Capturar datos del formulario
#        nombre = request.form.get('nombre')
#        correo_electronico = request.form.get('correo_electronico')
#        password = request.form.get('password')
#        pais = request.form.get('pais')
#        plan_suscripcion = request.form.get('plan_suscripcion')
#        dispositivos.append(request.form.get('dispositivos'))
#
#        # Crear el payload para enviar al microservicio
#        usuario_data = {
#            'nombre': nombre,
#            'correo_electronico': correo_electronico,
#            'password': password,
#            'pais': pais,
#            'plan_suscripcion': plan_suscripcion,
#            'dispositivos': dispositivos
#        }
#
#        # Hacer la solicitud POST al microservicio para crear el usuario
#        response = requests.post(
#            'http://localhost:8080/crear_usuario', json=usuario_data)
#
#        # Manejar la respuesta del microservicio
#        if response.status_code == 201:
#            flash('Usuario creado con éxito', 'success')
#            return redirect(url_for('login'))
#        else:
#            data = response.json()
#            flash(f"Error: {data['message']}", 'danger')
#
#    return render_template("crear_usuario.html")

# Obtener perfiles
# Moved
#@app.route('/perfiles')
#def obtener_perfiles():
#    # Se obtiene el usuario_id del usuario que se encuentra en la sesión
#    usuario_id = session.get('logged_user_id')
#
#    # Hacer la solicitud GET al microservicio para obtener los perfiles del usuario
#    response = requests.get(
#        'http://localhost:8080/usuario/' + str(usuario_id) + '/perfiles')
#
#    # Manejar la respuesta del microservicio
#    if response.status_code == 200:
#        data = response.json()
#        return render_template("perfiles.html", perfiles=data)
#    else:
#        data = response.json()
#        flash(f"Error: {data['message']}", 'danger')
#
#    return render_template("perfiles.html")


# Crear perfil
# Moved
#@app.route('/crear_perfil', methods=['GET', 'POST'])
#def crear_perfil():
#    if request.method == 'GET':
#        return render_template("crear_perfil.html")
#
#    if request.method == 'POST':
#        # Capturar datos del formulario
#        nombre = request.form.get('name')
#
#        # Se obtiene el usuario_id del usuario que se encuentra en la sesión
#        usuario_id = session.get('logged_user_id')
#
#        # Crear el payload para enviar al microservicio
#        perfil_data = {
#            'user_id': usuario_id,
#            'nombre': nombre,
#        }
#
#        # Hacer la solicitud POST al microservicio para crear el perfil
#        response = requests.post(
#            'http://localhost:8080/usuario/' + str(usuario_id) + '/perfiles', json=perfil_data)
#
#        # Manejar la respuesta del microservicio
#        if response.status_code == 201:
#            flash('Perfil creado con éxito', 'success')
#            return redirect(url_for('obtener_perfiles'))
#        else:
#            data = response.json()
#            flash(f"Error: {data['message']}", 'danger')
#
#    is_edit_str = request.args.get('is_edit', default='false')
#
#    # Convierte el string a booleano
#    is_edit = is_edit_str.lower() == 'true'
#
#    return render_template("crear_perfil.html", is_edit=is_edit)


@app.route('/inicio', methods=['GET'])
def pagina_inicio():
    perfil_id = request.args.get('perfil_id')
    usuario_id = session.get('logged_user_id')

    response = requests.get(
        'http://localhost:8080/usuario/' + str(usuario_id) + '/perfiles/' + perfil_id)

    if response.status_code == 200:
        data = response.json()
        return render_template("pagina_inicio.html", perfil=data)
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')

    return render_template("pagina_inicio.html")


# Moved
#@app.route('/cuenta', methods=['GET', 'POST'])
#def editar_usuario():
#    perfil_id = request.args.get('perfil_id', default='')
#    usuario_id = session.get('logged_user_id')
#
#    if request.method == 'GET':
#        response = requests.get(f'http://localhost:8080/usuario/{usuario_id}')
#        if response.status_code == 200:
#            data = response.json()
#            return render_template("crear_usuario.html", cuenta=data)
#        else:
#            data = response.json()
#            flash(f"Error: {data['message']}", 'danger')
#            # Redirigir a una vista de error si es necesario
#            return redirect(url_for('some_error_handling_view'))
#
#    if request.method == 'POST':
#        dispositivos = []
#        # Capturar datos del formulario
#        nombre = request.form.get('nombre')
#        correo_electronico = request.form.get('correo_electronico')
#        password = request.form.get('password')
#        pais = request.form.get('pais')
#        plan_suscripcion = request.form.get('plan_suscripcion')
#        dispositivos.append(request.form.get('dispositivos'))
#
#        # Verificación de campos obligatorios
#        if not nombre or not correo_electronico or not password:
#            flash("Todos los campos son obligatorios.", 'danger')
#            # Redirigir a la misma página para corregir
#            return redirect(url_for('editar_usuario'))
#
#        # Crear el payload para enviar al microservicio
#        usuario_data = {
#            'nombre': nombre,
#            'correo_electronico': correo_electronico,
#            'password': password,
#            'pais': pais,
#            'plan_suscripcion': plan_suscripcion,
#            'dispositivos': dispositivos
#        }
#
#        # Hacer la solicitud PUT al microservicio para actualizar el usuario
#        response = requests.put(
#            f'http://localhost:8080/actualizar_usuario/{usuario_id}', json=usuario_data)
#
#        if response.status_code == 200:
#            session['logged_user_name'] = nombre
#            flash("Usuario actualizado con éxito", 'success')
#            # Redirigir a la vista de perfiles
#            return redirect(url_for('obtener_perfiles'))
#        else:
#            data = response.json()
#            flash(f"Error: {data['message']}", 'danger')
#            # Redirigir a la misma página para corregir
#            return redirect(url_for('editar_usuario'))
#
#    # Si no se maneja el método, retornar a la página de cuenta o un error
#    # Cambia esto según sea necesario
#    return redirect(url_for('some_default_view'))
#
#
# Moved
#@app.route('/editar_perfil/<perfil_id>', methods=['GET', 'POST'])
#def editar_perfil(perfil_id):
#    usuario_id = session.get('logged_user_id')
#
#    # Método GET para cargar los datos del perfil
#    if request.method == 'GET':
#        response = requests.get(
#            f'http://localhost:8080/usuario/{usuario_id}/perfiles/{perfil_id}')
#
#        if response.status_code == 200:
#            data = response.json()
#            return render_template("crear_perfil.html", perfil=data, is_edit=True)
#        else:
#            # Manejar error en caso de no obtener datos del perfil
#            try:
#                data = response.json()
#                flash(
#                    f"Error: {data.get('message', 'No se pudo cargar el perfil.')}", 'danger')
#            except ValueError:
#                # Si no hay JSON en la respuesta (por ejemplo, error 500)
#                flash(
#                    "Error al cargar el perfil. El servidor no proporcionó una respuesta válida.", 'danger')
#            return redirect(url_for('obtener_perfiles'))
#
#    # Método POST para actualizar los datos del perfil
#    if request.method == 'POST':
#        nombre = request.form.get('name')
#
#        # Crear el payload para enviar al microservicio
#        perfil_data = {'nombre': nombre}
#
#        # Hacer la solicitud PUT para actualizar el perfil
#        response = requests.put(
#            f'http://localhost:8080/usuario/{usuario_id}/perfiles/{perfil_id}', json=perfil_data)
#
#        if response.status_code == 200:
#            flash("Perfil actualizado con éxito", 'success')
#            return redirect(url_for('obtener_perfiles'))
#        else:
#            # Manejar error en caso de no poder actualizar el perfil
#            try:
#                data = response.json()
#                flash(
#                    f"Error: {data.get('message', 'No se pudo actualizar el perfil.')}", 'danger')
#            except ValueError:
#                flash(
#                    "Error al actualizar el perfil. El servidor no proporcionó una respuesta válida.", 'danger')
#            return redirect(url_for('obtener_perfiles'))
#
# Moved
#@app.route('/eliminar_perfil/<perfil_id>', methods=['GET', 'POST'])
#def eliminar_perfil(perfil_id):
#    usuario_id = session.get('logged_user_id')
#
#    if request.method == 'GET':
#        print(perfil_id)
#        # Cargar los datos del perfil con disabilitado=True
#        response = requests.get(
#            f'http://localhost:8080/usuario/{usuario_id}/perfiles/{perfil_id}')
#        if response.status_code == 200:
#            data = response.json()
#            return render_template("crear_perfil.html", perfil=data, is_delete=True)
#        else:
#            data = response.json()
#            flash(f"Error: {data['message']}", 'danger')
#            return redirect(url_for('obtener_perfiles'))
#
#    if request.method == 'POST':
#        # Hacer la solicitud DELETE al microservicio para eliminar el perfil
#        response = requests.delete(
#            f'http://localhost:8080/usuario/{usuario_id}/perfiles/{perfil_id}')
#        print(response)
#        if response.status_code == 200:
#            flash("Perfil eliminado con éxito", 'success')
#            return redirect(url_for('obtener_perfiles'))
#        else:
#            data = response.json()
#            flash(f"Error: {data['message']}", 'danger')
#            return redirect(url_for('obtener_perfiles'))
#
# Moved
#@app.route('/borrar_cuenta')
#def borrar_cuenta():
#    usuario_id = session.get('logged_user_id')
#
#    response = requests.delete(
#        f'http://localhost:8080/eliminar_usuario/{usuario_id}')
#
#    if response.status_code == 200:
#        flash("Cuenta eliminada con éxito", 'success')
#        return redirect(url_for('cerrar_sesion'))
#    else:
#        data = response.json()
#        flash(f"Error: {data['message']}", 'danger')
#        return redirect(url_for('login'))
#
# Moved
#@app.route("/dispositivos", methods=['GET', 'POST'])
#def dispositivos():
#    if request.method == 'GET':
#        user_id = session.get('logged_user_id')
#        response = requests.get(
#            f'http://localhost:8080/usuario/{user_id}/dispositivos')
#        if response.status_code == 200:
#            data = response.json()
#            print (data)
#            return render_template("dispositivos.html", dispositivos=data)
#        else:
#            data = response.json()
#            flash(f"Error: {data['message']}", 'danger')
#            return redirect(url_for('obtener_perfiles'))
#    
# Moved
#@app.route("/crear_dispositivo", methods=['GET', 'POST'])
#def crear_dispositivo():
#    if request.method == 'GET':
#        return render_template("crear_dispositivo.html")
#   


@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
