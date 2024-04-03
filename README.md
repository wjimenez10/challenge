# Challenge ML

## Descripción ##

Para consumir los datos del endpoint propuesto en el challenge, se construyeron dos imagenes docker a fin de tener separados el ambiente de la base de datos y el de la aplicación.


(mymariadb): Este contenedor tiene una instancia de la base de datos relacional MariaDB con la base de datos y tabla creada. 

(myapp): Aplicación desarrollada en Python y Flask. Este contenedor contiene el código en Python y Flask, el cual proporciona una API para acceder y manipular los datos. La aplicación Flask se ejecuta en el puerto 5000 y se comunica con la base de datos MySQL en el contenedor mymariadb para almacenar los datos. 

## **Instalación y configuración del entorno MyAPP** ##

Este repositorio contiene los archivos necesarios para configurar y ejecutar el Challenge ML en cualquier servidor Linux utilizando Docker. 

## Requisitos previos a la instalación del ambiente. ##

1.- Tener instalado el ambiente docker en el sistema

2.- Tener instalado python3.



**Pasos para configurar y ejecutar el Challenge**


1.- Clonar el repositorio

    git clone https://github.com/wjimenez10/challenge.git


2.- Para construir los docker se deberán ejecutar los siguientes comandos:
   
    docker build -t mymariadb -f Dockerfile-MariaDB .
    docker build -t myapp .


3.- Iniciar los contenedores

    docker run -d --name mymariadb -p 3306:3306 mymariadb
    docker run -d --name myapp --link mymariadb myapp

**NOTA: Es mandatorio iniciar primero el contenedor mymariadb quien contiene la base de datos y luego la aplicación, ya que la aplicación intentará guardar la información del endpoint en la base de datos.**


4.- En el caso de necesitar realizar un stop/start de los contenedores se deberá ejecutar los siguientes comandos:

Parar contenedor:

    docker stop mymariadb 
    docker stop myapp

Iniciar contenedor:

    docker start mymariadb
    docker start myapp

6.- En caso de requerir analizar los logs de los contenedores se podrá ejecutar:

    docker logs mymariadb
    docker logs myapp

Ejemplo:   docker logs myapp

 * Serving Flask app 'challenge_MELI_app_v21'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on https://172.17.0.3:5000

**7.- Instalación desatendida**

Se ejecuta el instalador el cual realiza todos los pasos anteriores, genera el build de los docker, incia los contenedores.

    ./install.sh

Para el challenge la URL a utilizar en el browser es la siguiente: 

**https://172.17.0.3:5000**


7.-  # ENJOY #
