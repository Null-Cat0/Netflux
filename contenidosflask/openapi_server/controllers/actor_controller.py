import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.actor import Actor  # noqa: E501
from openapi_server.models.actor_update import ActorUpdate  # noqa: E501
from openapi_server.models.pelicula import Pelicula  # noqa: E501
from openapi_server.models.serie import Serie  # noqa: E501
from openapi_server import util


def actualizar_actor(actor_id, actor_update):  # noqa: E501
    """Actualizar un actor existente

    Actualiza la información de un actor específico por su ID. # noqa: E501

    :param actor_id: ID del actor a actualizar
    :type actor_id: int
    :param actor_update: Objeto del actor con la información actualizada
    :type actor_update: dict | bytes

    :rtype: Union[Actor, Tuple[Actor, int], Tuple[Actor, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        actor_update = ActorUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def crear_actor(actor):  # noqa: E501
    """Crear un nuevo actor

    Crea un nuevo actor con la información proporcionada. # noqa: E501

    :param actor: Objeto del actor a crear
    :type actor: dict | bytes

    :rtype: Union[Actor, Tuple[Actor, int], Tuple[Actor, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        actor = Actor.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def eliminar_actor(actor_id):  # noqa: E501
    """Eliminar un actor

    Elimina un actor específico por su ID. # noqa: E501

    :param actor_id: ID del actor a eliminar
    :type actor_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_actores():  # noqa: E501
    """Listar todos los actores

    Obtiene una lista de todos los actores registrados en el sistema. # noqa: E501


    :rtype: Union[List[Actor], Tuple[List[Actor], int], Tuple[List[Actor], int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_peliculas_de_actor(actor_id):  # noqa: E501
    """Listar películas en las que ha participado un actor en específico.

    Obtiene una lista de todas las películas en las que ha participado un actor. # noqa: E501

    :param actor_id: ID del actor
    :type actor_id: int

    :rtype: Union[List[Pelicula], Tuple[List[Pelicula], int], Tuple[List[Pelicula], int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_series_de_actor(actor_id):  # noqa: E501
    """Listar series en las que ha participado un actor en específico.

    Obtiene una lista de todas las series en las que ha participado un actor. # noqa: E501

    :param actor_id: ID del actor
    :type actor_id: int

    :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_actor(actor_id):  # noqa: E501
    """Obtener un actor específico

    Obtiene la información detallada de un actor específico por su ID. # noqa: E501

    :param actor_id: ID del actor a obtener
    :type actor_id: int

    :rtype: Union[Actor, Tuple[Actor, int], Tuple[Actor, int, Dict[str, str]]
    """
    return 'do some magic!'
