import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.recomendacion import Recomendacion  # noqa: E501
from openapi_server import util


def crear_recomendacion_perfil(perfil_id, recomendacion):  # noqa: E501
    """Crea una recomendación para un perfil

    Crea una recomendación para un perfil en específico # noqa: E501

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int
    :param recomendacion: ID del contenido a visualizar
    :type recomendacion: dict | bytes

    :rtype: Union[Recomendacion, Tuple[Recomendacion, int], Tuple[Recomendacion, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        recomendacion = Recomendacion.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def eliminar_recomendacion_perfil(perfil_id, recomendacion_id):  # noqa: E501
    """Elimina una recomendación en específico de un perfil

    Elimina una recomendación en específico de un perfil # noqa: E501

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int
    :param recomendacion_id: ID de la recomendacion especificada
    :type recomendacion_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_recomendacion_perfil(perfil_id, recomendacion_id):  # noqa: E501
    """Obtiene una recomendación en específico de un perfil

    Obtiene una recomendación en específico de un perfil # noqa: E501

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int
    :param recomendacion_id: ID de la recomendacion especificada
    :type recomendacion_id: int

    :rtype: Union[Recomendacion, Tuple[Recomendacion, int], Tuple[Recomendacion, int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_recomendaciones_perfil(perfil_id):  # noqa: E501
    """Obtiene una lista de las recomendaciones para el perfil

    Obtiene una lista de las recomendaciones para el perfil # noqa: E501

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int

    :rtype: Union[List[Recomendacion], Tuple[List[Recomendacion], int], Tuple[List[Recomendacion], int, Dict[str, str]]
    """
    return 'do some magic!'
