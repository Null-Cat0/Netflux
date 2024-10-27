import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
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
        response = requests.post('http://localhost:8080/iniciar_sesion', json=login_data)

        # Manejar la respuesta del microservicio
        if response.status_code == 200:
            data = response.json()
            flash(data['message'], 'success')
            #print(data['usuario'])

            session.permanent = True
            session['logged_user_id'] = data['usuario']['user_id']
            session['logged_user_name'] = data['usuario']['nombre']

            # Redirigir al perfil del usuario usando el user_id
            return redirect(url_for('obtener_perfiles'))
        else:
            data = response.json()
            flash(data['message'], 'danger')

    return render_template("inicio_sesion.html")

@app.route('/cerrar_sesion')
def cerrar_sesion():
    # Elimina 'logged_user_id' de la sesión para cerrar sesión
    session.pop('logged_user_id', None)
    flash("Has cerrado sesión con éxito.", "info")  # Mensaje opcional para el usuario
    return redirect(url_for('login'))  # Redirige a la página de inicio de sesión o a la página principal

@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'GET':
        # Renderiza el formulario de creación de cuenta

        return render_template("crear_usuario.html")

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
        response = requests.post('http://localhost:8080/crear_usuario', json=usuario_data)

        # Manejar la respuesta del microservicio
        if response.status_code == 201:
            flash('Usuario creado con éxito', 'success')
            return redirect(url_for('login'))
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')

    return render_template("crear_usuario.html")

#Obtener perfiles
@app.route('/perfiles')
def obtener_perfiles():
    # Se obtiene el usuario_id del usuario que se encuentra en la sesión
    usuario_id = session.get('logged_user_id')

    # Hacer la solicitud GET al microservicio para obtener los perfiles del usuario
    response = requests.get('http://localhost:8080/usuario/' + str(usuario_id) + '/perfiles')

    # Manejar la respuesta del microservicio
    if response.status_code == 200:
        data = response.json()
        print(data)
        return render_template("perfiles.html", perfiles=data)
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        
    return render_template("perfiles.html")


#Crear perfil
@app.route('/crear_perfil', methods=['GET', 'POST'])
def crear_perfil():
    if request.method == 'GET':
        return render_template("crear_perfil.html")
    
    if request.method == 'POST':
        # Capturar datos del formulario
        nombre = request.form.get('name')
        
        # Se obtiene el usuario_id del usuario que se encuentra en la sesión    
        usuario_id = session.get('logged_user_id')

        # Crear el payload para enviar al microservicio
        perfil_data = {
            'user_id': usuario_id,
            'nombre': nombre,
        }

        # Hacer la solicitud POST al microservicio para crear el perfil
        response = requests.post('http://localhost:8080/usuario/' + str(usuario_id) + '/perfiles', json=perfil_data)

        # Manejar la respuesta del microservicio
        if response.status_code == 201:
            flash('Perfil creado con éxito', 'success')
            return redirect(url_for('obtener_perfiles'))
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            
    is_edit_str = request.args.get('is_edit', default='false')
    
    # Convierte el string a booleano
    is_edit = is_edit_str.lower() == 'true'
    
    return render_template("crear_perfil.html", is_edit=is_edit)

@app.route('/inicio', methods=['GET'])
def pagina_inicio():
    perfil_id = request.args.get('perfil_id', default='')
    usuario_id = session.get('logged_user_id')
    
    response = requests.get('http://localhost:8080/usuario/' + str(usuario_id) + '/perfiles/' + perfil_id)
    
    if response.status_code == 200:
        data = response.json()
        return render_template("pagina_inicio.html", perfil=data)
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        
    return render_template("pagina_inicio.html")


@app.route('/cuenta', methods=['GET', 'POST'])
def editar_usuario():
    perfil_id = request.args.get('perfil_id', default='')
    usuario_id = session.get('logged_user_id')

    if request.method == 'GET':
        response = requests.get(f'http://localhost:8080/usuario/{usuario_id}')
        if response.status_code == 200:
            data = response.json()
            return render_template("crear_usuario.html", cuenta=data)
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            return redirect(url_for('some_error_handling_view'))  # Redirigir a una vista de error si es necesario

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
            return redirect(url_for('editar_usuario'))  # Redirigir a la misma página para corregir

        # Crear el payload para enviar al microservicio
        usuario_data = {
            'nombre': nombre,
            'correo_electronico': correo_electronico,
            'password': password,
            'pais': pais,
            'plan_suscripcion': plan_suscripcion,
            'dispositivos': dispositivos
        }

        print("Data usuario")
        print(usuario_data)

        # Hacer la solicitud PUT al microservicio para actualizar el usuario
        response = requests.put(f'http://localhost:8080/actualizar_usuario/{usuario_id}', json=usuario_data)

        if response.status_code == 200:
            session['logged_user_name'] = nombre
            flash("Usuario actualizado con éxito", 'success')
            return redirect(url_for('obtener_perfiles'))  # Redirigir a la vista de perfiles
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            return redirect(url_for('editar_usuario'))  # Redirigir a la misma página para corregir

    # Si no se maneja el método, retornar a la página de cuenta o un error
    return redirect(url_for('some_default_view'))  # Cambia esto según sea necesario


@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)