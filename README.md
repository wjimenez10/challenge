# Challenge ML

**Challenge ML - Configuración y Ejecución**

Este repositorio contiene los archivos necesarios para configurar y ejecutar el Challenge ML en cualquier servidor Linux utilizando Docker.

**Pasos para configurar y ejecutar el Challenge**

1.- Clonar el repositorio

git clone https://github.com/wjimenez10/url

2.- Requisito para la instalación de Docker

Es requisito tener instalado en el ambiente Docker y Docker-compose a fin de generar las imagenes docker.

3.- Para construir los docker se deberá ejecutar los siguientes comandos:
   
    docker build -t mymariadb -f Dockerfile-MariaDB .
    docker build -t myapp .

4.- Iniciar los contenedores

    docker run -d --name mymariadb -p 3306:3306 mymariadb
    docker run -d --name myapp --link mymariadb myapp

**NOTA: Es importante iniciar primero el contenedor mymariadb conteniendo la base de datos y luego la aplicación, ya que la aplicación intentará guardar la información del endpoint en la base de datos.**

5.- En el caso de necesitar realizar un stop/start de los contenedores se deberá ejecutar los siguientes comandos:

Parar contenedor:

    docker stop mymariadb 
    docker start mymariadb

Iniciar contenedor:

    docker stop myapp
    docker start myapp

6.- En caso de requerir analizar los logs de los contenedores se podrá ejecutar:

    docker logs mymariadb
    docker logs myapp

