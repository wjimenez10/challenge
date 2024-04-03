FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Crear la carpeta para los certificados de MariaDB
RUN mkdir -p certs/mariadb-certs

# Copia el script de la aplicación Python al contenedor

COPY challenge_MELI_app_v21.py .

# Copia los certificados al contenedor
COPY certs/cert.crt certs/cert.key .
COPY certs/mariadb-certs/cert.crt certs/mariadb-certs/cert.crt
COPY certs/mariadb-certs/private_key.pem certs/mariadb-certs/private_key.pem

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python
RUN pip install Flask requests mysqlclient

# Expone el puerto 5000 para acceder a la aplicación Flask (tanto HTTP como HTTPS)
EXPOSE 5000

# Ejecuta la aplicación Flask para que escuche en todas las interfaces
CMD ["python", "challenge_MELI_app_v21.py"]

