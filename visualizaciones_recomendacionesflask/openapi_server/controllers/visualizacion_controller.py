import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.visualizacion import Visualizacion  # noqa: E501
from openapi_server import util


def actualizar_visualizacion_capitulo_perfil(perfil_id, capitulo_id):  # noqa: E501
    """Actualiza la visualización de un capítulo por un perfil

    Actualiza el progreso de la visualización de un capítulo por un perfil # noqa: E501

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int
    :param capitulo_id: ID del capítulo especificado
    :type capitulo_id: int

    :rtype: Union[Capitulo, Tuple[Capitulo, int], Tuple[Capitulo, int, Dict[str, str]]
    """
    return 'do some magic!'


def actualizar_visualizacion_pelicula_perfil(perfil_id, pelicula_id):  # noqa: E501
    """Actualiza la visualización de la película por un perfil

    Actualiza el progreso de la visualización de la película por un perfil # noqa: E501

    :param perfil_id: ID del perfil específicado
    :type perfil_id: int
    :param pelicula_id: ID de la película a actualizar
    :type pelicula_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def crear_visualizacion_contenido_perfil(perfil_id, visualizacion):  # noqa: E501
    """Inicia la visualización de un capítulo o película por un perfil

    Inicia la visualización de un capítulo o película por un perfil # noqa: E501

    :param perfil_id: ID del perfil especificado
    :type perfil_id: int
    :param visualizacion: ID del contenido a visualizar
    :type visualizacion: dict | bytes

    :rtype: Union[Visualizacion, Tuple[Visualizacion, int], Tuple[Visualizacion, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        visualizacion = Visualizacion.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def listar_visualizaciones_contenido(contenido_id):  # noqa: E501
    """Lista de perfiles que han visto el contenido especificado

    Lista de perfiles que han visto el contenido especificado. # noqa: E501

    :param contenido_id: ID del perfil a obtener
    :type contenido_id: int

    :rtype: Union[List[Perfil], Tuple[List[Perfil], int], Tuple[List[Perfil], int, Dict[str, str]]
    """
    return 'do some magic!'


def listar_visualizaciones_perfil(perfil_id):  # noqa: E501
    """Historial de un perfil en específico

    Obtiene una lista de todos los capítulos o películas visualizados o en progreso por el perfil especificado. # noqa: E501

    :param perfil_id: ID del perfil a obtener
    :type perfil_id: int

    :rtype: Union[List[Visualizacion], Tuple[List[Visualizacion], int], Tuple[List[Visualizacion], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_visualizacion_capitulo_perfil(perfil_id, capitulo_id):  # noqa: E501
    """Obtiene el capítulo en visualización del perfil especificado

    Obtiene el capítulo en visualización por el perfil especificado. # noqa: E501

    :param perfil_id: ID del perfil a obtener
    :type perfil_id: int
    :param capitulo_id: ID del perfil a obtener
    :type capitulo_id: int

    :rtype: Union[List[Capitulo], Tuple[List[Capitulo], int], Tuple[List[Capitulo], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_visualizacion_pelicula_perfil(perfil_id, pelicula_id):  # noqa: E501
    """Obtiene la película visualizada por el perfil especificado

    Obtiene la película en visualización por el perfil especificado. # noqa: E501

    :param perfil_id: ID del perfil a obtener
    :type perfil_id: int
    :param pelicula_id: ID del perfil a obtener
    :type pelicula_id: int

    :rtype: Union[Pelicula, Tuple[Pelicula, int], Tuple[Pelicula, int, Dict[str, str]]
    """
    return 'do some magic!'
