import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.actor import Actor  # noqa: E501
from openapi_server.models.asignar_actor_a_serie_request import AsignarActorASerieRequest  # noqa: E501
from openapi_server.models.pelicula import Pelicula  # noqa: E501
from openapi_server.models.pelicula_update import PeliculaUpdate  # noqa: E501
from openapi_server import util


def actualizar_pelicula(pelicula_id, pelicula_update):  # noqa: E501
    """Actualizar una película existente

    Actualiza la información de una película específica por su ID. # noqa: E501

    :param pelicula_id: ID de la película a actualizar
    :type pelicula_id: int
    :param pelicula_update: Objeto de la película con la información actualizada
    :type pelicula_update: dict | bytes

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        pelicula_update = PeliculaUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def asignar_actor_a_pelicula(pelicula_id, asignar_actor_a_serie_request):  # noqa: E501
    """Asignar un actor a una película

    Asigna un actor existente a una película específica. # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int
    :param asignar_actor_a_serie_request: ID del actor a asignar
    :type asignar_actor_a_serie_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        asignar_actor_a_serie_request = AsignarActorASerieRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def crear_pelicula(pelicula):  # noqa: E501
    """Crear una nueva película

    Crea una nueva película con la información proporcionada. # noqa: E501

    :param pelicula: Objeto de la película a crear
    :type pelicula: dict | bytes

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        pelicula = Pelicula.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def eliminar_actor_pelicula(pelicula_id, actor_id):  # noqa: E501
    """Elimnar un actor de una película

    Elimina un actor existente de una película específica. # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int
    :param actor_id: ID del actor
    :type actor_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def eliminar_pelicula(pelicula_id):  # noqa: E501
    """Eliminar una película

    Elimina una película específica por su ID. # noqa: E501

    :param pelicula_id: ID de la película a eliminar
    :type pelicula_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_actores_de_pelicula(pelicula_id):  # noqa: E501
    """Listar actores de una película específica

    Obtiene una lista de todos los actores que participan en una película específica. # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int

    :rtype: Union[List[Actor], Tuple[List[Actor], int], Tuple[List[Actor], int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_peliculas():  # noqa: E501
    """Listar todas las películas

    Obtiene una lista de todas las películas disponibles en el sistema, incluyendo información básica como el título, género y año de estreno. # noqa: E501


    :rtype: Union[List[Pelicula], Tuple[List[Pelicula], int], Tuple[List[Pelicula], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_pelicula(pelicula_id):  # noqa: E501
    """Obtener una película específica

    Obtiene la información detallada de una película específica por su ID. # noqa: E501

    :param pelicula_id: ID de la película a obtener
    :type pelicula_id: int

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_precuela_pelicula(pelicula_id):  # noqa: E501
    """Obtiene la precuela de una película específica

    Obtiene la precuela de una película específica # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_secuela_pelicula(pelicula_id):  # noqa: E501
    """Obtiene la secuela de una película específica

    Obtiene la secuela de una película específica # noqa: E501

    :param pelicula_id: ID de la película
    :type pelicula_id: int

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    return 'do some magic!'
