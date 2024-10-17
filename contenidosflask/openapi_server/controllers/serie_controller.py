import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.actor import Actor  # noqa: E501
from openapi_server.models.asignar_actor_a_serie_request import AsignarActorASerieRequest  # noqa: E501
from openapi_server.models.serie import Serie  # noqa: E501
from openapi_server.models.serie_update import SerieUpdate  # noqa: E501
from openapi_server import util


def actualizar_serie(serie_id, serie_update):  # noqa: E501
    """Actualizar una serie existente

    Actualiza la información de una serie específica por su ID. # noqa: E501

    :param serie_id: ID de la serie a actualizar
    :type serie_id: int
    :param serie_update: Objeto de la serie con la información actualizada
    :type serie_update: dict | bytes

    :rtype: Union[Serie, Tuple[Serie, int], Tuple[Serie, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        serie_update = SerieUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def asignar_actor_a_serie(serie_id, asignar_actor_a_serie_request):  # noqa: E501
    """Asignar un actor a una serie

    Asigna un actor existente a una serie específica. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param asignar_actor_a_serie_request: ID del actor a asignar
    :type asignar_actor_a_serie_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        asignar_actor_a_serie_request = AsignarActorASerieRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def crear_serie(serie):  # noqa: E501
    """Crear una nueva serie

    Crea una nueva serie de televisión con la información proporcionada. # noqa: E501

    :param serie: Objeto de la serie a crear
    :type serie: dict | bytes

    :rtype: Union[Serie, Tuple[Serie, int], Tuple[Serie, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        serie = Serie.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def eliminar_actor_serie(serie_id, actor_id):  # noqa: E501
    """Elimnar un actor de una serie

    Elimina un actor existente de una serie específica. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param actor_id: ID del actor
    :type actor_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def eliminar_serie(serie_id):  # noqa: E501
    """Eliminar una serie

    Elimina una serie específica por su ID. # noqa: E501

    :param serie_id: ID de la serie a eliminar
    :type serie_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_actores_de_serie(serie_id):  # noqa: E501
    """Listar los actores de una serie específica

    Obtiene una lista de todos los actores que participan en una serie específica. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int

    :rtype: Union[List[Actor], Tuple[List[Actor], int], Tuple[List[Actor], int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_series():  # noqa: E501
    """Listar todas las series

    Obtiene una lista de todas las series de televisión disponibles en el sistema, incluyendo información básica como el título, género y año de estreno. # noqa: E501


    :rtype: Union[List[Serie], Tuple[List[Serie], int], Tuple[List[Serie], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_serie(serie_id):  # noqa: E501
    """Obtener una serie específica

    Obtiene la información detallada de una serie específica por su ID. # noqa: E501

    :param serie_id: ID de la serie a obtener
    :type serie_id: int

    :rtype: Union[Serie, Tuple[Serie, int], Tuple[Serie, int, Dict[str, str]]
    """
    return 'do some magic!'
