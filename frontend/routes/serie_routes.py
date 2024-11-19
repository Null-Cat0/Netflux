import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from global_config import ContenidosConfig as contConf
from global_config import UsuariosConfig as userConf

serie_bp = Blueprint('serie', __name__)

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
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/listar_generos")
            if response.status_code == 200:
                generos = response.json()
            else:
                generos = []
                
            # Obtener todos los actores
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/listar_actores")
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
            print(data)
            response = requests.post(f"{contConf.CONTENIDOS_BASE_URL}/crear_serie", json=data)
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
    response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/listar_series")
    print(f"Esadmin {es_admin}")
    if response.status_code == 200:
        series = response.json()
        return render_template("series.html", es_admin=es_admin, series=series)
    else:
        flash("Error al obtener la lista de series.", 'danger')
        return render_template("series.html")

@serie_bp.route('/serie/<serie_id>', methods=['GET'])
def serie(serie_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    return render_template("serie.html")

@serie_bp.route('/editar_serie/<serie_id>', methods=['GET', 'POST'])
def editar_serie(serie_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))

    es_admin = session.get('es_admin')
    if es_admin:
        if request.method == 'GET':
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/obtener_serie/{serie_id}")
            
            if response.status_code == 200:
                serie = response.json()
                
                # Obtener todos los generos
                response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/listar_generos")
                if response.status_code == 200:
                    generos = response.json()
                else:
                    generos = []
                    
                # Obtener todos los actores
                response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/listar_actores")
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
            response = requests.put(f"{contConf.CONTENIDOS_BASE_URL}/actualizar_serie/{serie_id}", json=data)
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
        response = requests.delete(f"{contConf.CONTENIDOS_BASE_URL}/eliminar_serie/{serie_id}")
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
            n_temporada = request.form.get('n_temporada')
            anio_estreno = request.form.get('anio_estreno')
            data = {
                "numero": n_temporada,
                "anio_estreno": anio_estreno
            }

            response = requests.post(f"{contConf.CONTENIDOS_BASE_URL}/asignar_temporada_serie/{serie_id}", json=data)
            if response.status_code == 201:
                flash("Temporada creada exitosamente.", 'success')
                return redirect(url_for('serie.listar_series'))
            else:
                flash("Error al crear la temporada.", 'danger')
                return render_template("formulario_temporada.html")
    else:
        flash("No tienes permisos para realizar esta acción.", 'danger')
        return redirect(url_for('serie.listar_series'))
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
            response = requests.get(f"{contConf.CONTENIDOS_BASE_URL}/obtener_temporada_serie/{serie_id}/{temporada_id}")
            if response.status_code == 200:
                return render_template("formulario_temporada.html", temporada=response.json())
        
        if request.method == 'POST':
            n_temporada = request.form.get('n_temporada')
            anio_estreno = request.form.get('anio_estreno')
            data = {
                "n_temporada": n_temporada,
                "anio_estreno": anio_estreno
            }

            response = requests.put(f"{contConf.CONTENIDOS_BASE_URL}/actualizar_temporada_serie/{serie_id}/{temporada_id}", json=data)
            if response.status_code == 200:
                flash("Temporada editada exitosamente.", 'success')
                return redirect(url_for('serie.listar_series'))
            else:
                flash("Error al editar la temporada.", 'danger')
                return render_template("formulario_temporada.html")
    else:
        flash("No tienes permisos para realizar esta acción.", 'danger')
        return redirect(url_for('serie.listar_series'))
    
    return render_template("formulario_temporada.html")

@serie_bp.route('/eliminar_temporada/<serie_id>/<temporada_id>', methods=['GET'])
def eliminar_temporada(serie_id, temporada_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    es_admin = session.get('es_admin')
    if es_admin:
        response = requests.delete(f"{contConf.CONTENIDOS_BASE_URL}/eliminar_temporada_serie/{serie_id}/{temporada_id}")
        if response.status_code == 200:
            flash("Temporada eliminada exitosamente.", 'success')
        else:
            flash("Error al eliminar la temporada.", 'danger')
        
        return redirect(url_for('serie.listar_series'))
    else:
        flash("No tienes permisos para realizar esta acción.", 'danger')
        return redirect(url_for('serie.listar_series'))
    
    return redirect(url_for('serie.listar_temporadas'))

@serie_bp.route('/crear_capitulo', methods=['GET', 'POST'])
def crear_capitulo():
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    # Se obtiene el usuario correspondiente al ID y se comprueba si es admin
    
    if request.method == 'GET':
        return render_template("formulario_capitulo.html")
    
    if request.method == 'POST':
        return render_template("formulario_capitulo.html")
    
    return render_template("formulario_capitulo.html")

@serie_bp.route('/editar_capitulo/<capitulo_id>', methods=['GET', 'POST'])
def editar_capitulo(capitulo_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    if request.method == 'GET':
        return render_template("formulario_capitulo.html")
    
    if request.method == 'POST':
        return render_template("formulario_capitulo.html")
    
    return render_template("formulario_capitulo.html")

@serie_bp.route('/eliminar_capitulo/<capitulo_id>', methods=['GET'])
def eliminar_capitulo(capitulo_id):
    usuario_id = session.get('logged_user_id')
    if not usuario_id:
        flash("Usuario no autenticado.", 'danger')
        return redirect(url_for('user.login'))
    
    return redirect(url_for('serie.listar_capitulos'))
