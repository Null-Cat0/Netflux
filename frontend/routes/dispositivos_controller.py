import requests
from flask import request, render_template, flash, redirect, url_for, session

@app.route("/dispositivos", methods=['GET', 'POST'])
def dispositivos():
    if request.method == 'GET':
        user_id = session.get('logged_user_id')
        response = requests.get(
            f'http://localhost:8080/usuario/{user_id}/dispositivos')
        if response.status_code == 200:
            data = response.json()
            print (data)
            return render_template("dispositivos.html", dispositivos=data)
        else:
            data = response.json()
            flash(f"Error: {data['message']}", 'danger')
            return redirect(url_for('obtener_perfiles'))
    
@app.route("/crear_dispositivo", methods=['GET', 'POST'])
def crear_dispositivo():
    if request.method == 'GET':
        return render_template("crear_dispositivo.html")