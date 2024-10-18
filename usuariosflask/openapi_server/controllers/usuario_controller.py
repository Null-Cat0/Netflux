import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from sqlalchemy.util import methods_equivalent


from openapi_server.models.usuario import Usuario  # noqa: E501
from openapi_server.models.usuario_update import UsuarioUpdate  # noqa: E501
from openapi_server import util
from openapi_server import db

# Importa la app de Flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from openapi_server.models.perfil import Perfil
from openapi_server.models.usuario import Usuario

from openapi_server import connex_app, app

def actualizar_usuario(user_id, usuario_update):  # noqa: E501
    """Actualizar un usuario existente

    Actualiza la información de un usuario específico por su ID. # noqa: E501

    :param user_id: ID del usuario a actualizar
    :type user_id: int
    :param usuario_update: Objeto del usuario con la información actualizada
    :type usuario_update: dict | bytes

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        usuario_update = UsuarioUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

# Esto no tira con el parametro de usuario colocado, el resto si


@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():  # noqa: E501
    """Crear un nuevo usuario

    Crea un nuevo usuario con la información proporcionada. # noqa: E501

    :param usuario: Objeto del usuario a crear
    :type usuario: dict | bytes

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """

    if request.method == 'POST':
        # Procesar el formulario cuando se hace el submit
        nombre = request.form.get('nombre')
        correo_electronico = request.form.get('correo_electronico')
        password=request.form.get('password')
        pais = request.form.get('pais')
        plan_suscripcion = request.form.get('plan_suscripcion')
        dispositivos = request.form.get('dispositivos')

        # Aquí puedes crear un objeto de usuario y guardarlo en la base de datos
        nuevo_usuario = Usuario(
            nombre=nombre,
            correo_electronico=correo_electronico,
            password=password,
            pais=pais,
            plan_suscripcion=plan_suscripcion,
            dispositivos=dispositivos
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario creado con éxito', 'success')
        return redirect(url_for('login'))

    # Si el método es GET, renderizamos el formulario
    return render_template('crear_usuario.html')


def eliminar_usuario(user_id):  # noqa: E501
    """Eliminar un usuario

    Elimina un usuario específico por su ID. # noqa: E501

    :param user_id: ID del usuario a eliminar
    :type user_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_usuarios():  # noqa: E501
    """Listar todos los usuarios

    Obtiene una lista de todos los usuarios disponibles en el sistema. # noqa: E501


    :rtype: Union[List[Usuario], Tuple[List[Usuario], int], Tuple[List[Usuario], int, Dict[str, str]]
    """
    return 'do some magic!'


@app.route('/usuario/<user_id>', methods=['GET', 'POST'])
def obtener_usuario(user_id):  # noqa: E501
    """Obtener un usuario específico

    Obtiene la información detallada de un usuario específico por su ID. # noqa: E501

    :param user_id: ID del usuario a obtener
    :type user_id: int

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    return f'do some magic, {user_id}!'
