import requests
import MySQLdb
from datetime import datetime
from flask import Flask, jsonify
import re

# Función para ofuscar el número de tarjeta de crédito
def mask_credit_card(credit_card_num):
    return "X" * (len(credit_card_num) - 4) + credit_card_num[-4:]

# Función para ofuscar el CCV
def mask_ccv(credit_card_ccv):
    return "XXX"

# Función para ofuscar el número de cuenta
def mask_account_number(account_number):
    return "X" * (len(account_number) - 4) + account_number[-4:]

# Configuración de la conexión a la base de datos MariaDB con SSL
conexion = MySQLdb.connect(
    user="meli",
    password="meli123",
    host="mymariadb",
    port=3306,
    database="Challenge_MELI_db",
    ssl={
        "cert": "certs/mariadb-certs/cert.crt",  # Ruta del certificado
        "key": "certs/mariadb-certs/private_key.pem",    # Ruta de la clave privada
        "ca": "certs/mariadb-certs/cert.crt"        # Ruta del certificado de la autoridad de certificación
    }
)

cursor = conexion.cursor()

# Creación de la aplicación Flask
app = Flask(__name__)

# Endpoint para obtener todos los usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    try:
        # Consulta SQL para obtener todos los usuarios de la base de datos
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        # Transforma los resultados de la consulta en un formato JSON y los devuelve
        resultados = []
        for usuario in usuarios:
            usuario_dict = {
                "id": usuario[0],
                "fec_alta": usuario[1],
                "user_name": usuario[2],
                "codigo_zip": usuario[3],
                "credit_card_num": mask_credit_card(usuario[4]),
                "credit_card_ccv": mask_ccv(usuario[5]),
                "cuenta_numero": mask_account_number(usuario[6]),
                "direccion": usuario[7],
                "geo_latitud": usuario[8],
                "geo_longitud": usuario[9],
                "color_favorito": usuario[10],
                "foto_dni": usuario[11],
                "ip": usuario[12],
                "auto_marca": usuario[13],
                "auto_modelo": usuario[14],
                "auto_tipo": usuario[15],
                "auto_color": usuario[16],
                "cantidad_compras": usuario[17],
                "avatar": usuario[18],
                "fec_birthday": usuario[19]
            }
            resultados.append(usuario_dict)

        return jsonify(resultados)
    except MySQLdb.Error as e:
        print(f"Error al obtener usuarios: {e}")
        return jsonify({"error": "Error al obtener usuarios"}), 500

if __name__ == "__main__":
    # Realiza una solicitud GET al endpoint proporcionado por el proveedor externo
    url = "https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios"
    response = requests.get(url)
    data = response.json()

    # Inserta los datos de usuarios en la base de datos MariaDB
    try:
        for usuario in data:
            # Comprobar si el usuario ya existe en la base de datos
            cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE id = %s)", (usuario["id"],))
            result = cursor.fetchone()[0]

            if not result:
                # Truncar el campo 'credit_card_num' si es demasiado largo
                credit_card_num = usuario["credit_card_num"][:20]

                # Convertir la fecha de alta al formato adecuado
                try:
                    fec_alta = datetime.strptime(usuario["fec_alta"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    fec_alta = datetime.strptime(usuario["fec_alta"], '%d/%m/%Y').strftime('%Y-%m-%d %H:%M:%S')

                # Convertir la fecha de cumpleaños al formato adecuado
                try:
                    fec_birthday = datetime.strptime(usuario["fec_birthday"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    fec_birthday = datetime.strptime(usuario["fec_birthday"], '%d/%m/%Y').strftime('%Y-%m-%d %H:%M:%S')

                # Insertar el usuario en la base de datos
                cursor.execute("""
                    INSERT INTO usuarios (id, fec_alta, user_name, codigo_zip, credit_card_num, credit_card_ccv, cuenta_numero, direccion, geo_latitud, geo_longitud, color_favorito, foto_dni, ip, auto_marca, auto_modelo, auto_tipo, auto_color, cantidad_compras, avatar, fec_birthday)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    usuario["id"], fec_alta, usuario["user_name"], usuario["codigo_zip"], 
                    credit_card_num, usuario["credit_card_ccv"], usuario["cuenta_numero"], 
                    usuario["direccion"], usuario["geo_latitud"], usuario["geo_longitud"], 
                    usuario["color_favorito"], usuario["foto_dni"], usuario["ip"], 
                    usuario["auto"], usuario["auto_modelo"], usuario["auto_tipo"], 
                    usuario["auto_color"], usuario["cantidad_compras_realizadas"], usuario["avatar"], 
                    fec_birthday
                ))

        conexion.commit()
        print("Datos insertados correctamente en la base de datos.")
    except MySQLdb.Error as e:
        print(f"Error al insertar datos en la base de datos: {e}")

    # Configuración del contexto SSL/TLS
    ssl_context = ('cert.crt', 'cert.key')
    # Ejecuta la aplicación Flask con el contexto SSL/TLS
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=ssl_context)

