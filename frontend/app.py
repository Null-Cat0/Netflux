from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'secret_key'

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
            # Redirigir al perfil del usuario usando el user_id
            #return redirect(url_for('obtener_usuario', user_id=data['user_id']))
            print(data)
        else:
            data = response.json()
            flash(data['message'], 'danger')

    return render_template("inicio_sesion.html")

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

@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)