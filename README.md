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
