# Netflux
Proyecto de la asignatura ASEE.

# Componentes de la aplicación
Este proyecto está compuesto por cuatro componentes, tres microservicios y el frontend.

## Contenidos
El microservicio de *contenidos* se encuentra la carpeta **contenidosflask**.

## Usuarios
El microservicio de *usuarios* se encuentra la carpeta **usuariosflask**.

## Visualizaciones y Recomendaciones
El microservicio de *visualizaciones y recomendaciones* se encuentra la carpeta **visualizaciones_recomendacionesflask**.

## Frontend
El frontend es la parte encargada de gestionar la *interfaz de usuario* de la aplicación, encontrándose en la carpeta **frontend**.

# Ejecución con contenedores
## Creación de los directorios para los datos de las bases de datos
Debido a que se usa almacenamiento persistente, se tienen asociadas rutas del sistema de archivos de la máquina host al almacenamiento de los datos de las bases de datos. Para asegurar que estas son desplegadas de manera correcta, se recomienda crear estos directorios con los siguientes comandos:
```bash
# Desde la carpeta raíz del proyecto
mkdir databases/mongodb/mondodb_data
mkdir databases/mysql/mysql_data
```

## Despliegue
Para desplegar el proyecto, desde la carpeta raíz se debe ejecutar el siguiente comando:
```bash
docker-compose build
docker-compose up -d
```

# Cambios reentrega 2
- Ruta con dos métodos ha sido actualizada, ya que daba conflicto con la ruta GET de /usuarios
```python
# usuario_controller.py
## Antes
@app.route('/usuarios', methods=['GET', 'POST'])
## Después
@app.route('/usuarios', methods=['POST'])
```

- Faltaba una '/' en una ruta relacionada con la creación de capítulos en una temporada
```python
# serie_routes.py
## Antes
response = requests.post(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas{temporada_id}/capitulos", json=data)
## Después
response = requests.post(f"{contConf.CONTENIDOS_BASE_URL}/series/{serie_id}/temporadas/{temporada_id}/capitulos", json=data)
```
- Debido a algunos problemas a la hora de levantar el microservicio de usuarios, se ha incluido un `sleep` antes de iniciar la conexión para intentar dar tiempo al contenedor del MySQL a inicializarse.
```python
db = SQLAlchemy()
sleep(2)
db.init_app(app)
```
