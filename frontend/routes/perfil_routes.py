import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime

from global_config import UsuariosConfig as userConf
from global_config import ContenidosConfig as contConf
from global_config import VisualizacionesConfig as visConf

perfil_bp = Blueprint('perfil', __name__)

def actualizar_datos_historial(usuario_id, perfil_id, contenido_id):    

    response = requests.patch(f"{visConf.VISUALIZACIONES_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}/visualizaciones/{contenido_id}")

    if response.status_code != 200:
        data = response.json()
        flash(f"{data['message']}", 'danger')

    # Se actualiza el contenido en el historial del perfil
    response = requests.patch(f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}/historial/{contenido_id}")
    if response.status_code != 200:
        data = response.json()
        flash(f"{data['message']}", 'danger')

    flash("Contenido actualizado en el historial", 'success')

@perfil_bp.route('/perfiles')
def obtener_perfiles():
    # Se obtiene el usuario_id del usuario que se encuentra en la sesión
    usuario_id = session.get('logged_user_id')
    session.pop('perfil_id', None)
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))

    # Hacer la solicitud GET al microservicio para obtener los perfiles del usuario
    response = requests.get(
        f"{userConf.USUARIOS_BASE_URL}/usuarios/{str(usuario_id)}/perfiles")

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
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))  # Asegúrate de tener una ruta de login
    
    if request.method == 'GET':
        requests_generos = requests.get(f'{contConf.CONTENIDOS_BASE_URL}/generos')
        if requests_generos.status_code == 200:
            generos = requests_generos.json()
            return render_template("formulario_perfil.html", generos=generos)
        else:
            flash("Error al cargar los géneros", 'danger')
            return redirect(url_for('perfil.obtener_perfiles'))

    if request.method == 'POST':
        # Comprobación de que tiene 5 o menos perfiles
        response = requests.get(
        f"{userConf.USUARIOS_BASE_URL}/usuarios/{str(usuario_id)}/perfiles")

        if response.status_code == 200:
            data = response.json()
            if len(data) >= 4:
                flash("No puedes tener más de 4 perfiles", 'danger')
                return redirect(url_for('perfil.obtener_perfiles'))
        else:   
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            return redirect(url_for('perfil.obtener_perfiles'))
        
        
        # Capturar datos del formulario
        nombre = request.form.get('name')
        foto_perfil = request.form.get('foto_perfil') or 'netflux_rojo.png'  # Asignar por defecto si está vacío

        # Validar que el nombre no esté vacío
        if not nombre:
            flash('El nombre del perfil es obligatorio.', 'danger')
            return redirect(url_for('crear_perfil'))

        # Validar 'foto_perfil' contra las imágenes permitidas
        imagenes_permitidas = ['netflux_amarillo.png', 'netflux_azul.png', 'netflux_rojo.png', 'netflux_verde.png']
        if foto_perfil not in imagenes_permitidas:
            flash("Imagen no válida.", 'danger')
            return redirect(url_for('crear_perfil'))

        # Validar las preferencias de contenido
        subtitulos = request.form.get('subtitulos') == 'on'
        idioma_audio = request.form.get('idioma_audio')
        generos = request.form.getlist('generos')  # Lista de géneros seleccionados
         
        # Crear el payload para enviar al microservicio
        perfil_data = {
            'user_id': usuario_id,
            'nombre': nombre,
            'foto_perfil': foto_perfil,
            'preferencias_contenido': {
                'subtitulos': subtitulos,
                'idioma_audio': 'es' if idioma_audio == 'default' else idioma_audio,
                'generos': generos
            }
        }

        # Hacer la solicitud POST al microservicio para crear el perfil
        response = requests.post(
            f"{userConf.USUARIOS_BASE_URL}/usuarios/{str(usuario_id)}/perfiles", json=perfil_data)

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
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))

    # Método GET para cargar los datos del perfil
    if request.method == 'GET':
        response = requests.get(
            f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}")

        if response.status_code == 200:
            data = response.json()
            response_generos = requests.get(f'{contConf.CONTENIDOS_BASE_URL}/generos')
            if response_generos.status_code == 200:
                generos = response_generos.json()
                return render_template("formulario_perfil.html", perfil=data, generos=generos, is_edit=True)
            else:
                flash("Error al cargar los géneros", 'danger')
                return redirect(url_for('perfil.obtener_perfiles'))
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
        foto_perfil = request.form.get('foto_perfil')

        # Retrieve preferences data from form fields
        subtitulos = request.form.get('subtitulos') == 'on'
        idioma_audio = request.form.get('idioma_audio')
        generos = request.form.getlist('generos') # List from selected genres

        # Crear el payload para enviar al microservicio
        perfil_data = {
            'nombre': nombre,
            'foto_perfil': foto_perfil,
            'preferencias_contenido': {
                'subtitulos': subtitulos,
                'idioma_audio': idioma_audio,
                'generos': generos
            }
        }
        
        # Hacer la solicitud PUT para actualizar el perfil
        response = requests.put(
            f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}", json=perfil_data)

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
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))

    # Hacer la solicitud DELETE al microservicio para eliminar el perfil
    response = requests.delete(
        f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}")
                
    if response.status_code == 200:
        flash("Perfil eliminado con éxito", 'success')
        return redirect(url_for('perfil.obtener_perfiles'))
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        return redirect(url_for('perfil.obtener_perfiles'))

@perfil_bp.route('/mi_lista/<perfil_id>', methods=['GET'])
def obtener_mi_lista(perfil_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Debes iniciar sesión para acceder a esta página", 'danger')
        return redirect(url_for('user.login'))
    
    response = requests.get(f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}/lista")
    
    # Manejar la respuesta del microservicio
    if response.status_code == 200:
        data = response.json()
        return render_template("mi_lista.html", peliculas=data['peliculas'], series=data['series'])
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        
    return render_template("mi_lista.html")

@perfil_bp.route('/agregar_a_lista_perfil/<perfil_id>/<contenido_id>', methods=['GET','POST'])
def agregar_a_lista_perfil(perfil_id, contenido_id,):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Debes iniciar sesión para acceder a esta página", 'danger')
        return redirect(url_for('user.login'))
    
    response = requests.post(f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}/lista/{contenido_id}")
    if response.status_code == 201:
        flash("Contenido agregado a la lista", 'success')
    else:
        data = response.json()
        flash(f"{data['message']}", 'warning')
        
    referer = request.referrer.split('/')[-1]
    if referer == 'mi_lista':
        return redirect(url_for('perfil.obtener_mi_lista', perfil_id=perfil_id))
    elif referer.split('?')[0] == 'inicio':
        return redirect(url_for('pagina_inicio', perfil_id=perfil_id))
    elif referer == 'lista_series':
        return redirect(url_for('serie.obtener_series'))
    else:
        return redirect(url_for('pelicula.obtener_peliculas'))

@perfil_bp.route('/eliminar_de_lista_perfil/<perfil_id>/<contenido_id>', methods=['GET','POST'])
def eliminar_de_lista_perfil(perfil_id, contenido_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Debes iniciar sesión para acceder a esta página", 'danger')
        return redirect(url_for('user.login'))
    
    response = requests.delete(f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}/lista/{contenido_id}")
    if response.status_code == 200:
        flash("Contenido eliminado de la lista", 'success')
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
    return redirect(url_for('perfil.obtener_mi_lista', perfil_id=perfil_id))  

@perfil_bp.route('/mi_historial/<perfil_id>', methods=['GET'])
def obtener_mi_historial(perfil_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Debes iniciar sesión para acceder a esta página", 'danger')
        return redirect(url_for('user.login'))
    
    response = requests.get(f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}/historial")
    # Manejar la respuesta del microservicio
    if response.status_code == 200:
        data = response.json()
       
        historial = []
        capitulos = data["capitulos"]
        peliculas = data["peliculas"]
        
        for capitulo in capitulos:
            capitulo["fecha_visualizacion"] = datetime.strptime(capitulo["fecha_visualizacion"], '%a, %d %b %Y %H:%M:%S %Z').strftime('%d/%m/%Y')
            historial.append(capitulo)
            
        for pelicula in peliculas:
            pelicula["fecha_visualizacion"] = datetime.strptime(pelicula["fecha_visualizacion"], '%a, %d %b %Y %H:%M:%S %Z').strftime('%d/%m/%Y')
            historial.append(pelicula)
            
        # Se ordena el historial por fecha de visualización
        historial = sorted(historial, key=lambda x: datetime.strptime(x["fecha_visualizacion"], '%d/%m/%Y'), reverse=True)
        
        return render_template("mi_historial.html", historial=historial)
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        
    return render_template("mi_historial.html")  

@perfil_bp.route('/agregar_a_historial_perfil/<perfil_id>/<contenido_id>', methods=['GET','POST'])
def agregar_a_historial_perfil(perfil_id, contenido_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Debes iniciar sesión para acceder a esta página", 'danger')
        return redirect(url_for('user.login'))
    
    serie_id = request.form.get('serie_id')
    temporada_id = request.form.get('temporada_id')
    
    # Se obtiene el contenido correspondiente al contenido_id
    if serie_id and temporada_id:
        response = requests.get(f"{visConf.VISUALIZACIONES_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}/visualizaciones/capitulos/{contenido_id}")
        if response.status_code == 200:
            actualizar_datos_historial(usuario_id, perfil_id, contenido_id)
        else:
            data = {
                'serie_id': serie_id,
                'temporada_id': temporada_id,
                'capitulo_id': contenido_id
            }
            response = requests.post(f"{visConf.VISUALIZACIONES_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}/visualizaciones", json=data)
            if response.status_code == 201:
                flash("Contenido agregado al historial", 'success')
            else:
                data = response.json()
                flash(f"{data['message']}", 'danger')
    else:
        data = {
            'pelicula_id': contenido_id
        }
        # Se busca si el contenido ya está en el historial
        response = requests.get(f"{visConf.VISUALIZACIONES_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}/visualizaciones/peliculas/{contenido_id}")
        if response.status_code == 200:
            actualizar_datos_historial(usuario_id, perfil_id, contenido_id)
        else:
            response = requests.post(f"{visConf.VISUALIZACIONES_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}/visualizaciones", json=data)
            if response.status_code == 201:
                flash("Contenido agregado al historial", 'success')
            else:
                data = response.json()
                flash(f"{data['message']}", 'danger')

    referer = request.referrer.split('/')[-1]
    if referer.split('?')[0] == 'inicio':
        return redirect(url_for('pagina_inicio', perfil_id=perfil_id))
    elif referer == 'lista_series':
        return redirect(url_for('serie.obtener_series'))
    else:
        return redirect(url_for('pelicula.obtener_peliculas'))
    
@perfil_bp.route('/eliminar_de_historial_perfil/<perfil_id>/<contenido_id>', methods=['GET','POST'])
def eliminar_de_historial_perfil(perfil_id, contenido_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Debes iniciar sesión para acceder a esta página", 'danger')
        return redirect(url_for('user.login'))
    
    response = requests.delete(f"{visConf.VISUALIZACIONES_BASE_URL}/usuarios/{usuario_id}/perfiles/{perfil_id}/visualizaciones/{contenido_id}")
    if response.status_code == 200:
        flash("Contenido eliminado del historial", 'success')
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        
    return redirect(url_for('perfil.obtener_mi_historial', perfil_id=perfil_id))