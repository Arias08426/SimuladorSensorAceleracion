# Importar las librerías necesarias
import firebase_admin  # Librería para interactuar con Firebase
from firebase_admin import db  # Módulo de base de datos en tiempo real de Firebase
from flask import Flask, request, jsonify, render_template  # Flask para crear la API, gestionar solicitudes y renderizar plantillas HTML
from datetime import datetime  # Para trabajar con fechas y horas
from firebase_admin.exceptions import FirebaseError  # Manejar errores específicos de Firebase
from flask_cors import CORS  # Habilitar CORS para permitir solicitudes desde diferentes orígenes

# Inicializar Firebase
path = 'project_credentials.json'  # Ruta al archivo de credenciales de Firebase
url = "https://sensores-3ba4f-default-rtdb.firebaseio.com/"  # URL de la base de datos en tiempo real de Firebase

# Inicializa la aplicación de Firebase usando las credenciales y el URL de la base de datos
firebase_admin.initialize_app(firebase_admin.credentials.Certificate(path), {
    'databaseURL': url
})

# Inicializar la aplicación Flask
app = Flask(__name__)  # Crea la aplicación Flask

@app.route('/')  # Define la ruta raíz ('/')
def home():
    # Renderiza una página HTML de inicio
    return render_template('index.html')

# Habilitar CORS para aceptar solicitudes de diferentes dominios
CORS(app)

# Definir la referencia principal de la base de datos Firebase
fb_db_ref = db.reference('/sensor_data')  # Referencia al nodo `sensor_data` en la base de datos

# Ruta para guardar datos de sensores (método POST)
@app.route('/api/sensor_data', methods=['POST'])
def save_sensor_data():
    """
    Endpoint para guardar datos enviados por sensores.
    """
    try:
        # Obtener los datos enviados en el cuerpo de la solicitud (en formato JSON)
        data = request.get_json()
        if not data:  # Verifica si el cuerpo de la solicitud está vacío
            return jsonify({"error": "El cuerpo de la solicitud está vacío"}), 400

        # Extraer los valores necesarios del JSON recibido
        idsensor = data.get('idsensor')  # ID del sensor
        valor = data.get('valor')  # Valor de la lectura del sensor

        # Validar que los campos obligatorios existan
        if not idsensor or valor is None:
            return jsonify({"error": "Los campos 'idsensor' y 'valor' son obligatorios"}), 400

        # Generar un timestamp para incluir en el registro
        timestamp = datetime.now()  # Obtiene la fecha y hora actuales
        record = {
            "fecha": timestamp.strftime("%Y-%m-%d"),  # Fecha en formato AAAA-MM-DD
            "hora": timestamp.strftime("%H:%M:%S"),  # Hora en formato HH:MM:SS
            "idsensor": idsensor,  # ID del sensor
            "valor": valor  # Valor de la lectura
        }

        # Guardar los datos en Firebase, generando automáticamente un ID único
        fb_db_ref.push(record)

        # Responder con un mensaje de éxito y los datos registrados
        return jsonify({"message": "Datos del sensor guardados con éxito", "data": record}), 200

    # Manejar errores específicos de Firebase
    except FirebaseError as e:
        return jsonify({"error": f"Error de Firebase: {str(e)}"}), 500

    # Manejar cualquier otro tipo de error inesperado
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

# Ruta para obtener todos los datos de los sensores (método GET)
@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    """
    Endpoint para obtener todos los datos almacenados de sensores.
    """
    try:
        # Obtener todos los datos del nodo `sensor_data` en Firebase
        data = fb_db_ref.get()

        # Si no hay datos, devuelve un mensaje indicando que no se encontraron registros
        if not data:
            return jsonify({"message": "No se encontraron datos de sensores", "data": []}), 200

        # Convierte los datos (un diccionario) a una lista de registros con sus IDs
        sensor_data_list = [{"id": key, **value} for key, value in data.items()]

        # Responde con los datos obtenidos
        return jsonify({"data": sensor_data_list}), 200

    # Manejar errores específicos de Firebase
    except FirebaseError as e:
        return jsonify({"error": f"Error de Firebase: {str(e)}"}), 500

    # Manejar cualquier otro tipo de error inesperado
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

# Ejecutar la aplicación Flask
if __name__ == "__main__":
    # Ejecuta la aplicación en modo depuración, permitiendo acceso desde cualquier host y en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
