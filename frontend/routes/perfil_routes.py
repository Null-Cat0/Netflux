import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from global_config import UsuariosConfig as userConf

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/perfiles')
def obtener_perfiles():
    # Se obtiene el usuario_id del usuario que se encuentra en la sesión
    usuario_id = session.get('logged_user_id')

    # Hacer la solicitud GET al microservicio para obtener los perfiles del usuario
    response = requests.get(
        f"{userConf.USUARIOS_BASE_URL}/usuario/{str(usuario_id)}/perfiles")

    # Manejar la respuesta del microservicio
    if response.status_code == 200:
        data = response.json()
        return render_template("perfiles.html", perfiles=data)
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')

    return render_template("perfiles.html")

@perfil_bp.route('/crear_perfil', methods=['GET', 'POST'])
def crear_perfil():
    if request.method == 'GET':
        return render_template("formulario_perfil.html")

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
        response = requests.post(
            f"{userConf.USUARIOS_BASE_URL}/usuario/{str(usuario_id)}/perfiles", json=perfil_data)

        # Manejar la respuesta del microservicio
        if response.status_code == 201:
            flash('Perfil creado con éxito', 'success')
            return redirect(url_for('perfil.obtener_perfiles'))
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')

        is_edit_str = request.args.get('is_edit', default='false')

        # Convierte el string a booleano
        is_edit = is_edit_str.lower() == 'true'

        return render_template("formulario_perfil.html", is_edit=is_edit)

@perfil_bp.route('/editar_perfil/<perfil_id>', methods=['GET', 'POST'])
def editar_perfil(perfil_id):
    usuario_id = session.get('logged_user_id')

    # Método GET para cargar los datos del perfil
    if request.method == 'GET':
        response = requests.get(
            f"{userConf.USUARIOS_BASE_URL}/usuario/{usuario_id}/perfiles/{perfil_id}")

        if response.status_code == 200:
            data = response.json()
            return render_template("formulario_perfil.html", perfil=data, is_edit=True)
        else:
            # Manejar error en caso de no obtener datos del perfil
            try:
                data = response.json()
                flash(
                    f"Error: {data.get('message', 'No se pudo cargar el perfil.')}", 'danger')
            except ValueError:
                # Si no hay JSON en la respuesta (por ejemplo, error 500)
                flash(
                    "Error al cargar el perfil. El servidor no proporcionó una respuesta válida.", 'danger')
            return redirect(url_for('perfil.obtener_perfiles'))

    # Método POST para actualizar los datos del perfil
    if request.method == 'POST':
        nombre = request.form.get('name')

        # Crear el payload para enviar al microservicio
        perfil_data = {'nombre': nombre}

        # Hacer la solicitud PUT para actualizar el perfil
        response = requests.put(
            f"{userConf.USUARIOS_BASE_URL}/usuario/{usuario_id}/perfiles/{perfil_id}", json=perfil_data)

        if response.status_code == 200:
            flash("Perfil actualizado con éxito", 'success')
            return redirect(url_for('perfil.obtener_perfiles'))
        else:
            # Manejar error en caso de no poder actualizar el perfil
            try:
                data = response.json()
                flash(
                    f"Error: {data.get('message', 'No se pudo actualizar el perfil.')}", 'danger')
            except ValueError:
                flash(
                    "Error al actualizar el perfil. El servidor no proporcionó una respuesta válida.", 'danger')
            return redirect(url_for('perfil.obtener_perfiles'))

@perfil_bp.route('/eliminar_perfil/<perfil_id>', methods=['GET', 'POST'])
def eliminar_perfil(perfil_id):
    usuario_id = session.get('logged_user_id')

    if request.method == 'GET':
        print(perfil_id)
        # Cargar los datos del perfil con disabilitado=True
        response = requests.get(
            f"{userConf.USUARIOS_BASE_URL}/usuario/{usuario_id}/perfiles/{perfil_id}")
        if response.status_code == 200:
            data = response.json()
            return render_template("formulario_perfil.html", perfil=data, is_delete=True)
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            return redirect(url_for('perfil.obtener_perfiles'))

    if request.method == 'POST':
        # Hacer la solicitud DELETE al microservicio para eliminar el perfil
        response = requests.delete(
            f"{userConf.USUARIOS_BASE_URL}/usuario/{usuario_id}/perfiles/{perfil_id}")
                
        print(response)
        if response.status_code == 200:
            flash("Perfil eliminado con éxito", 'success')
            return redirect(url_for('perfil.obtener_perfiles'))
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            return redirect(url_for('perfil.obtener_perfiles'))
