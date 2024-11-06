import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from global_config import ContenidosConfig as contConf

contenidos_bp = Blueprint('contenidos', __name__)

@contenidos_bp.route('/peliculas')
def peliculas():
    return render_template("peliculas.html")

@contenidos_bp.route('/series')
def series():
    return render_template("series.html")

