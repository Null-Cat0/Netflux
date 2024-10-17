import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.temporada import Temporada  # noqa: E501
from openapi_server.models.temporada_update import TemporadaUpdate  # noqa: E501
from openapi_server import util


def actualizar_temporada(serie_id, temporada_id, temporada_update):  # noqa: E501
    """Actualizar una temporada existente

    Actualiza la información de una temporada específica de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int
    :param temporada_update: Objeto de la temporada con la información actualizada
    :type temporada_update: dict | bytes

    :rtype: Union[Temporada, Tuple[Temporada, int], Tuple[Temporada, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        temporada_update = TemporadaUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def crear_temporada(serie_id, temporada):  # noqa: E501
    """Crear una nueva temporada para una serie

    Crea una nueva temporada para una serie específica. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada: Objeto de la temporada a crear
    :type temporada: dict | bytes

    :rtype: Union[Temporada, Tuple[Temporada, int], Tuple[Temporada, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        temporada = Temporada.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def eliminar_temporada(serie_id, temporada_id):  # noqa: E501
    """Eliminar una temporada

    Elimina una temporada específica de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_temporadas(serie_id):  # noqa: E501
    """Listar todas las temporadas de una serie

    Obtiene una lista de todas las temporadas de una serie específica. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int

    :rtype: Union[List[Temporada], Tuple[List[Temporada], int], Tuple[List[Temporada], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_temporada(serie_id, temporada_id):  # noqa: E501
    """Obtener una temporada específica de una serie

    Obtiene la información detallada de una temporada específica de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int

    :rtype: Union[Temporada, Tuple[Temporada, int], Tuple[Temporada, int, Dict[str, str]]
    """
    return 'do some magic!'
