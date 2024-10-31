import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import signal

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
    perfil_id = request.args.get('perfil_id')
    usuario_id = session.get('logged_user_id')

    response = requests.get(
        f"{Config.USUARIOS.USUARIOS_BASE_URL}/{str(usuario_id)}/perfiles/{perfil_id}")

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

# Signal handler for cleanup
def handle_shutdown(sig, frame):
    """Clear session data on server shutdown"""
    print("Shutting down and clearing session data")
    session.clear() # Clear session data
    sys.exit()

# Register the signals
signal.signal(signal.SIGINT, handle_shutdown)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
