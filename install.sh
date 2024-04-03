#!/bin/bash
##################################################
#						  #
#  Script para construir las contenedores docker  #
#						  #
#  myapp - Docker de aplicacion			  #
#  mymariadb - Docker de la base de datos MariaDB #
#						  #
#				Walter J	  #
###################################################
echo "Construyendo las imágenes Docker..."
docker build -t mymariadb -f Dockerfile-MariaDB .
docker build -t myapp .
if [ $? -ne 0 ]; then
    echo "Error: No se pudieron construir las imágenes Docker."
    exit 1
fi
echo "Imágenes Docker construidas exitosamente."

# Iniciar los contenedores
echo "Iniciando los contenedores..."
docker run -d --name mymariadb -p 3306:3306 mymariadb
sleep 15
docker run -d --name myapp --link mymariadb myapp

if [ $? -ne 0 ]; then
    echo "Error: No se pudieron iniciar los contenedores."
    exit 1
fi
echo "Contenedores iniciados exitosamente."
docker logs myapp
exit 0

