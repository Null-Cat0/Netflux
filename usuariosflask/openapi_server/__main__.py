#!/usr/bin/env python3
from sqlalchemy import values
from openapi_server.controllers import usuario_controller

from openapi_server import db
from openapi_server import connex_app, app

from flask import Flask, render_template, request, redirect, url_for, flash

from openapi_server.models import usuario
from openapi_server.models.usuario import Usuario

# Definir una ruta básica para verificar que la app funcione
@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("inicio_sesion.html")

    if request.method == 'POST':
        correo_electronico = request.form.get('correo')
        password = request.form.get('password')

        usuario_encontrado = Usuario.query.filter_by(correo_electronico=correo_electronico).first()

        if usuario_encontrado == None:
            flash("El correo introducido no existe", "danger")
        elif usuario_encontrado.password != password:
            flash("CONTRASEÑA INVÁLIDA (COMO TÚ)", "danger")
        else:
            return redirect(url_for('obtener_usuario', user_id=usuario_encontrado.user_id))

    return render_template("inicio_sesion.html")

@app.route('/')
def home():
    return redirect(url_for('login'))

# Punto de entrada principal
if __name__ == '__main__':
    # Crear las tablas de la base de datos al inicio de la app
    with app.app_context():
        db.create_all()
    connex_app.run(port=8080)
