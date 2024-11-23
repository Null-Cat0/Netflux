import os, sys, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, url_for, flash, session
from global_config import Config
from routes import blueprints

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.permanent_session_lifetime = Config.PERMANENT_SESSION_LIFETIME

for bp in blueprints:
    app.register_blueprint(bp)

@app.route('/inicio', methods=['GET'])
def pagina_inicio():
    if session.get('perfil_id') is None:
        perfil_id = request.args.get('perfil_id')
        session['perfil_id'] = perfil_id
    else:
        perfil_id = session.get('perfil_id')
    usuario_id = session.get('logged_user_id')

    response = requests.get(
        f"{Config.USUARIOS.USUARIOS_BASE_URL}/usuario/{str(usuario_id)}/perfiles/{perfil_id}")

    peliculas, series = [], []
    if response.status_code == 200:
        data = response.json()

        response_peliculas = requests.get(f"{Config.CONTENIDOS.CONTENIDOS_BASE_URL}/listar_peliculas")
        if response_peliculas.status_code == 200:
            peliculas = response_peliculas.json()

        response_series = requests.get(f"{Config.CONTENIDOS.CONTENIDOS_BASE_URL}/listar_series")
        if response_series.status_code == 200:
            series = response_series.json()

        response_recomendaciones = requests.get(
            f"{Config.VISUALIZACIONES.VISUALIZACIONES_BASE_URL}/usuario/{str(usuario_id)}/perfil/{perfil_id}/recomendacion")

        recomendaciones_pelicula = []
        recomendaciones_serie = []
        if response_recomendaciones.status_code == 200:
            recomendaciones = response_recomendaciones.json()
            recomendaciones_pelicula = recomendaciones.get('peliculas', [])
            recomendaciones_serie = recomendaciones.get('series', [])

            rs,rp = [],[]
            for recomendacion in recomendaciones_pelicula:
                response = requests.get(f"{Config.CONTENIDOS.CONTENIDOS_BASE_URL}/obtener_pelicula/{recomendacion}")
                if response.status_code == 200:
                    rp.append(response.json())
            
            for recomendacion in recomendaciones_serie:
                response = requests.get(f"{Config.CONTENIDOS.CONTENIDOS_BASE_URL}/obtener_serie/{recomendacion}")
                if response.status_code == 200:
                    rs.append(response.json())

        else:
            flash(f"Error al obtener las recomendaciones", 'danger')

        return render_template(
            "pagina_inicio.html",
            perfil=data,
            peliculas=peliculas,
            series=series,
            recomendaciones_pelicula=rp,
            recomendaciones_serie=rs
        )
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')
        return render_template("pagina_inicio.html")



@app.route('/')
def home():
    return redirect(url_for('user.login'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
