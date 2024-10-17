import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.capitulo import Capitulo  # noqa: E501
from openapi_server.models.capitulo_update import CapituloUpdate  # noqa: E501
from openapi_server import util


def actualizar_capitulo(serie_id, temporada_id, capitulo_id, capitulo_update):  # noqa: E501
    """Actualizar un capítulo existente

    Actualiza la información de un capítulo específico de una temporada de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int
    :param capitulo_id: ID del capítulo
    :type capitulo_id: int
    :param capitulo_update: Objeto del capítulo con la información actualizada
    :type capitulo_update: dict | bytes

    :rtype: Union[Capitulo, Tuple[Capitulo, int], Tuple[Capitulo, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        capitulo_update = CapituloUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def crear_capitulo(serie_id, temporada_id, capitulo):  # noqa: E501
    """Crear un nuevo capítulo para una temporada

    Crea un nuevo capítulo para una temporada específica de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int
    :param capitulo: Objeto del capítulo a crear
    :type capitulo: dict | bytes

    :rtype: Union[Capitulo, Tuple[Capitulo, int], Tuple[Capitulo, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        capitulo = Capitulo.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def eliminar_capitulo(serie_id, temporada_id, capitulo_id):  # noqa: E501
    """Eliminar un capítulo

    Elimina un capítulo específico de una temporada de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int
    :param capitulo_id: ID del capítulo
    :type capitulo_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_capitulos(serie_id, temporada_id):  # noqa: E501
    """Listar todos los capítulos de una temporada

    Obtiene una lista de todos los capítulos de una temporada específica de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int

    :rtype: Union[List[Capitulo], Tuple[List[Capitulo], int], Tuple[List[Capitulo], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_capitulo(serie_id, temporada_id, capitulo_id):  # noqa: E501
    """Obtener un capítulo específico de una temporada

    Obtiene la información detallada de un capítulo específico de una temporada de una serie. # noqa: E501

    :param serie_id: ID de la serie
    :type serie_id: int
    :param temporada_id: ID de la temporada
    :type temporada_id: int
    :param capitulo_id: ID del capítulo
    :type capitulo_id: int

    :rtype: Union[Capitulo, Tuple[Capitulo, int], Tuple[Capitulo, int, Dict[str, str]]
    """
    return 'do some magic!'
