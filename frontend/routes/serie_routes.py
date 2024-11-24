import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from global_config import ContenidosConfig as contConf
from global_config import UsuariosConfig as userConf
from global_config import VisualizacionesConfig as visConf

serie_bp = Blueprint('serie', __name__)

def actualizar_visualizaciones_eliminar_capitulos(lista_capitulos):
    response = requests.get(f"{userConf.USUARIOS_BASE_URL}/usuarios")
    if response.status_code != 200:
        flash("Error al obtener la lista de usuarios.", 'danger')
        return redirect(url_for('serie.obtener_series'))
    usuarios = response.json()

    perfiles = []
    for usuario in usuarios:
        response = requests.get(f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario['user_id']}/perfiles")
        if response.status_code != 200:
            flash("Error al obtener la lista de perfiles.", 'danger')
            return redirect(url_for('serie.obtener_series'))
        perfiles += response.json()

    for perfil in perfiles:
        user_id = perfil['user_id']
        perfil_id = perfil['perfil_id']

        for capitulo in lista_capitulos:
            capitulo_id = capitulo['capitulo_id']

            response = requests.delete(f"{visConf.VISUALIZACIONES_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}/visualizaciones/{capitulo_id}")

            if response.status_code not in [200, 404]:
                flash(f"Error al eliminar las visualizaciones del perfil {perfil.id}.", 'danger')
                return redirect(url_for('serie.obtener_series'))

    # Si se llega a este punto, se eliminaron todas las visualizaciones de los capítulos
    return True

@serie_bp.route('/crear_serie', methods=['GET', 'POST'])
def crear_serie():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    es_admin = session.get('es_admin')

    if es_admin:
        if request.method == 'GET':
            # Obtener todos los generos
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/generos")
            if response.status_code == 200:
                generos = response.json()
            else:
                generos = []
                
            # Obtener todos los actores
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/actores")
            if response.status_code == 200:
                actores = response.json()
            else:
                actores = []
            
            return render_template("formulario_serie.html", actores=actores, generos=generos, es_admin=es_admin, serie={})

        if request.method == 'POST':
            nombre = request.form.get('titulo')
            sinopsis = request.form.get('sinopsis')
            anio = request.form.get('anio_estreno')
            genero = request.form.getlist('generos')
            actores = request.form.getlist('actores')
            data={
                "titulo": nombre,
                "sinopsis": sinopsis,
                "anio_estreno": anio,
                "actores": actores,
                "genero": genero
            }
            
            response = requests.post(f"{contConf.CONTENIDOS_BASE_URL}/series", json=data)
            if response.status_code == 201:
                flash("Serie creada exitosamente.", 'success')
                return redirect(url_for('serie.obtener_series'))
            else:
                flash("Error al crear la serie.", 'danger')
                return redirect(url_for('serie.obtener_series'))

    return render_template("formulario_serie.html")

@serie_bp.route('/lista_series', methods=['GET'])
def obtener_series():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
        # Obtener el usuario correspondiente al ID y comprobar si es admin
    
    es_admin = session.get('es_admin')
    
    response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/series")
    
    if response.status_code == 200:
        series = response.json()
        return render_template("series.html", es_admin=es_admin, series=series)
    else:
        flash("Error al obtener la lista de series.", 'danger')
        return render_template("series.html")

@serie_bp.route('/editar_serie/<serie_id>', methods=['GET', 'POST'])
def editar_serie(serie_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))

    es_admin = session.get('es_admin')
    if es_admin:
        if request.method == 'GET':
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}")
            
            if response.status_code == 200:
                serie = response.json()
                
                # Obtener todos los generos
                response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/generos")
                if response.status_code == 200:
                    generos = response.json()
                else:
                    generos = []
                    
                # Obtener todos los actores
                response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/actores")
                if response.status_code == 200:
                    actores = response.json()
                else:
                    actores = []
                
                return render_template("formulario_serie.html", serie=serie, generos=generos, actores=actores, es_admin=es_admin)
            else:
                try:
                    data = response.json()
                    flash(data.get('message', 'Error al obtener la serie.'), 'danger')
                except requests.exceptions.JSONDecodeError:
                    flash("Error al obtener la serie.", 'danger')
                return redirect(url_for('serie.obtener_series'))
            
        if request.method == 'POST':
            nombre = request.form.get('titulo')
            descripcion = request.form.get('sinopsis')
            anio = request.form.get('anio_estreno')
            genero = request.form.getlist('generos')
            actores = request.form.getlist('actores')
            data={
                "titulo": nombre,
                "sinopsis": descripcion,
                "anio_estreno": anio,
                "actores": actores,
                "genero": genero
            }
            response = requests.put(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}", json=data)
            if response.status_code == 200:
                flash("Serie editada exitosamente.", 'success')
                return redirect(url_for('serie.obtener_series'))
            else:
                flash("Error al editar la serie.", 'danger')
                return redirect(url_for('serie.obtener_series'))
        
@serie_bp.route('/eliminar_serie/<serie_id>', methods=['GET'])
def eliminar_serie(serie_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    if es_admin:
        # Antes de eliminar la serie, se deben eliminar todas las visualizaciones y recomendaciones asociadas
        # Se obtienen los capítulos de la serie
        response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}")
        if response.status_code != 200:
            flash("Error al obtener la serie.", 'danger')
            return redirect(url_for('serie.obtener_series'))

        serie = response.json()
        temporadas = serie['temporadas']
        capitulos = []
        for temporada in temporadas:
            capitulos += temporada['capitulos']

        response = requests.get(f"{userConf.USUARIOS_BASE_URL}/usuarios")
        if response.status_code != 200:
            flash("Error al obtener la lista de usuarios.", 'danger')
            return redirect(url_for('serie.obtener_series'))
        usuarios = response.json()

        perfiles = []
        for usuario in usuarios:
            response = requests.get(f"{userConf.USUARIOS_BASE_URL}/usuarios/{usuario['user_id']}/perfiles")
            if response.status_code != 200:
                flash("Error al obtener la lista de perfiles.", 'danger')
                return redirect(url_for('serie.obtener_series'))
            perfiles += response.json()

        # Se eliminan las visualizaciones asociadas a los capítulos
        for perfil in perfiles:
            user_id = perfil['user_id']
            perfil_id = perfil['perfil_id']

            for capitulo in capitulos:
                capitulo_id = capitulo['capitulo_id']

                response = requests.delete(f"{visConf.VISUALIZACIONES_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}/visualizaciones/{capitulo_id}")

                if response.status_code not in [200, 404]:
                    flash(f"Error al eliminar las visualizaciones del perfil {perfil.id}.", 'danger')
                    return redirect(url_for('serie.obtener_series'))

            # Se eliminan las referencias a la serie en las recomendaciones
            response = requests.get(f"{visConf.VISUALIZACIONES_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}/recomendaciones")
            if response.status_code != 200:
                flash("Error al obtener las recomendaciones.", 'danger')
                return redirect(url_for('serie.obtener_series'))
            recomendaciones = response.json()

            lista_series = recomendaciones['series']
            if serie_id in lista_series:
                lista_series.remove(serie_id) 
                response = requests.patch(f"{visConf.VISUALIZACIONES_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}/recomendaciones", json={"series_recomendadas": lista_series})
                if response.status_code != 200:
                    flash("Error al actualizar las recomendaciones.", 'danger')
                    return redirect(url_for('serie.obtener_series'))

            # Se borra el contenido de la lista del perfil
            response = requests.delete(f"{userConf.USUARIOS_BASE_URL}/usuarios/{user_id}/perfiles/{perfil_id}/lista/{serie_id}")
            if response.status_code not in [200, 404]: # 404 si no existe la lista
                flash("Error al eliminar la serie de la lista del perfil.", 'danger')
                return redirect(url_for('serie.obtener_series'))

        # Se elimina la serie
        response = requests.delete(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}")
        if response.status_code == 200:
            flash("Serie eliminada exitosamente.", 'success')
        else:
            flash("Error al eliminar la serie.", 'danger')
            
        return redirect(url_for('serie.obtener_series'))
    else:
        flash("No tienes permisos para realizar esta acción.", 'danger')
        return redirect(url_for('serie.obtener_series'))

@serie_bp.route('/crear_temporada/<serie_id>', methods=['GET', 'POST'])
def crear_temporada(serie_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    
    if es_admin:
        if request.method == 'GET':
            return render_template("formulario_temporada.html")
        
        if request.method == 'POST':
            numero = request.form.get('numero')
            anio_lanzamiento = request.form.get('anio_lanzamiento')
            data = {
                "numero": numero,
                "anio_lanzamiento": anio_lanzamiento
            }

            response = requests.post(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas", json=data)
            if response.status_code == 201:
                flash("Temporada creada exitosamente.", 'success')
                return redirect(url_for('serie.obtener_series'))
            else:
                flash("Error al crear la temporada.", 'danger')
                return render_template("formulario_temporada.html")
    else:
        flash("No tienes permisos para realizar esta acción.", 'danger')
        return redirect(url_for('serie.obtener_series'))
    return render_template("formulario_temporada.html")

@serie_bp.route('/editar_temporada/<serie_id>/<temporada_id>', methods=['GET', 'POST'])
def editar_temporada(serie_id, temporada_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    if es_admin:
        if request.method == 'GET':
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas/{temporada_id}")
            if response.status_code == 200:
                return render_template("formulario_temporada.html", temporada=response.json())
        
        if request.method == 'POST':
            numero = request.form.get('numero')
            anio_lanzamiento = request.form.get('anio_lanzamiento')
            data = {
                "numero": numero,
                "anio_lanzamiento": anio_lanzamiento
            }

            response = requests.put(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas/{temporada_id}", json=data)
            if response.status_code == 200:
                flash("Temporada editada exitosamente.", 'success')
                return redirect(url_for('serie.obtener_series'))
            else:
                flash("Error al editar la temporada.", 'danger')
                return render_template("formulario_temporada.html")
    else:
        flash("No tienes permisos para realizar esta acción.", 'danger')
        return redirect(url_for('serie.obtener_series'))
    
    return render_template("formulario_temporada.html")

@serie_bp.route('/eliminar_temporada/<serie_id>/<temporada_id>', methods=['GET'])
def eliminar_temporada(serie_id, temporada_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    if es_admin:
        # Se obtienen los capítulos de la temporada
        response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas/{temporada_id}")
        if response.status_code != 200:
            flash("Error al obtener la temporada.", 'danger')
            return redirect(url_for('serie.obtener_series'))

        temporada = response.json()
        capitulos = temporada['capitulos']

        state = actualizar_visualizaciones_eliminar_capitulos(capitulos)
        if not state:
            flash("Error al eliminar las visualizaciones de los capítulos.", 'danger')
            return redirect(url_for('serie.obtener_series'))

        response = requests.delete(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas/{temporada_id}")

        if response.status_code == 200:
            flash("Temporada eliminada exitosamente.", 'success')
        else:
            flash("Error al eliminar la temporada.", 'danger')
        
        return redirect(url_for('serie.obtener_series'))
    else:
        flash("No tienes permisos para realizar esta acción.", 'danger')
        return redirect(url_for('serie.obtener_series'))
    

@serie_bp.route('/crear_capitulo/<serie_id>/<temporada_id>', methods=['GET', 'POST'])
def crear_capitulo(serie_id, temporada_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    
    if es_admin:
        if request.method == 'GET':
            return render_template("formulario_capitulo.html")
        
        if request.method == 'POST':
            numero = request.form.get('numero')
            titulo = request.form.get('titulo')
            duracion = request.form.get('duracion')
            sinopsis = request.form.get('sinopsis')
            data = {
                "numero": numero,
                "titulo": titulo,
                "duracion": duracion,
                "sinopsis": sinopsis
            }

            response = requests.post(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas{temporada_id}/capitulos", json=data)
            if response.status_code == 201:
                flash("Capítulo creado exitosamente.", 'success')
                return redirect(url_for('serie.obtener_series'))
            else:
                flash("Error al crear el capítulo.", 'danger')
                return render_template("formulario_capitulo.html")
    else:
        flash("No tienes permisos para realizar esta acción.", 'danger')
        return redirect(url_for('serie.obtener_series'))
    return render_template("formulario_capitulo.html")

@serie_bp.route('/editar_capitulo/<serie_id>/<temporada_id>/<capitulo_id>', methods=['GET', 'POST'])
def editar_capitulo(serie_id, temporada_id, capitulo_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    
    if es_admin:
        if request.method == 'GET':
            
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas/{temporada_id}/capitulos/{capitulo_id}")
            if response.status_code == 200:
                return render_template("formulario_capitulo.html", capitulo=response.json())
            else:
                flash("Error al obtener el capítulo.", 'danger')
        
        if request.method == 'POST':
            numero = request.form.get('numero')
            titulo = request.form.get('titulo')
            duracion = request.form.get('duracion')
            sinopsis = request.form.get('sinopsis')
            data = {
                "numero": numero,
                "titulo": titulo,
                "duracion": duracion,
                "sinopsis": sinopsis
            }
            
            response = requests.put(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas/{temporada_id}/capitulos/{capitulo_id}", json=data)
            if response.status_code == 200:
                flash("Capítulo editado exitosamente.", 'success')
                return redirect(url_for('serie.obtener_series'))
            else:
                flash("Error al editar el capítulo.", 'danger')
                return render_template("formulario_capitulo.html")
    else:
        flash("No tienes permisos para realizar esta acción.", 'danger')
        return redirect(url_for('serie.obtener_series'))    
    return render_template("formulario_capitulo.html")

@serie_bp.route('/eliminar_capitulo/<serie_id>/<temporada_id>/<capitulo_id>', methods=['GET'])
def eliminar_capitulo(serie_id, temporada_id, capitulo_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    if es_admin:
        state = actualizar_visualizaciones_eliminar_capitulos([
            { "capitulo_id": capitulo_id }
        ])
        if not state:
            flash("Error al eliminar las visualizaciones del capítulo.", 'danger')
            return redirect(url_for('serie.obtener_series'))

        response = requests.delete(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas/{temporada_id}/capitulos/{capitulo_id}")
        if response.status_code == 200:
            flash("Capítulo eliminado exitosamente.", 'success')
        else:
            flash("Error al eliminar el capítulo.", 'danger')
        
        return redirect(url_for('serie.obtener_series'))
    else:
        flash("No tienes permisos para realizar esta acción.", 'danger')
        return redirect(url_for('serie.obtener_series'))
