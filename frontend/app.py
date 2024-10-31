import os
import requests

from flask import Flask, render_template, request, redirect, url_for, flash, session
from routes import blueprints
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv("../config.env")
USUARIOS_BASE_URL = os.getenv("USUARIOS_BASE_URL")
CONTENIDOS_BASE_URL = os.getenv("CONTENIDOS_BASE_URL")
VISUALIZACIONES_BASE_URL = os.getenv("VISUALIZACIONES_BASE_URL")


app = Flask(__name__)
app.secret_key = 'secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

for bp in blueprints:
    app.register_blueprint(bp)

@app.route('/inicio', methods=['GET'])
def pagina_inicio():
    perfil_id = request.args.get('perfil_id')
    usuario_id = session.get('logged_user_id')

    response = requests.get(
        # 'http://localhost:8080/usuario/' + str(usuario_id) + '/perfiles/' + perfil_id)
        f"{USUARIOS_BASE_URL}/{str(usuario_id)}/perfiles/{perfil_id}")

    if response.status_code == 200:
        data = response.json()
        return render_template("pagina_inicio.html", perfil=data)
    else:
        data = response.json()
        flash(f"Error: {data['message']}", 'danger')

    return render_template("pagina_inicio.html")


@app.route('/')
def home():
    return redirect(url_for('user.login'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
