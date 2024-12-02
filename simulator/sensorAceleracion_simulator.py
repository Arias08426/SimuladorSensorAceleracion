# Importa las librerías necesarias
import requests  # Para realizar solicitudes HTTP
import random  # Para generar valores aleatorios
import time  # Para gestionar el tiempo en la simulación
import math  # Para cálculos matemáticos como funciones trigonométricas
import sys  # Para interactuar con el sistema, como salir del programa

class AccelerationSensorSimulator:
    """
    Clase para simular un sensor de aceleración.
    """
    def __init__(self, sensor_id, base_url, interval=30):
        """
        Inicializa el simulador de sensores de aceleración.

        Args:
            sensor_id (str): Identificador único del sensor (formato típico: HHHH1234).
            base_url (str): URL base de la API Flask donde se enviarán los datos.
            interval (int): Intervalo de tiempo entre lecturas en segundos.
        """
        self.sensor_id = sensor_id  # Identificador único del sensor
        self.base_url = base_url.rstrip('/')  # Elimina una barra final si está presente en la URL base
        self.interval = interval  # Intervalo entre lecturas (en segundos)
        self.last_value = 0.0  # Valor inicial de aceleración, simulando un vehículo en reposo

    def generate_realistic_value(self):
        """
        Genera un valor de aceleración realista basado en variaciones aleatorias y patrones periódicos.

        Returns:
            float: Un valor representando la aceleración en m/s².
        """
        # Genera un cambio aleatorio pequeño entre -0.5 y 0.5 para simular pequeñas variaciones
        change = random.uniform(-0.5, 0.5)

        # Simula una variación periódica, como las causadas por giros o vibraciones del vehículo
        time_factor = math.sin(time.time() / 60) * 2

        # Calcula el nuevo valor de aceleración basado en el último valor, el cambio y el factor de tiempo
        new_value = self.last_value + change + time_factor

        # Limita el valor dentro de un rango realista de aceleración (-10 m/s² a 10 m/s²)
        new_value = max(-10, min(10, new_value))

        # Actualiza el último valor para futuras iteraciones
        self.last_value = new_value

        # Redondea el valor a dos decimales para mayor precisión
        return round(new_value, 2)

    def send_reading(self):
        """
        Envía una lectura del sensor a la API definida en base_url.
        """
        # Crea un diccionario que representa la lectura del sensor
        reading = {
            'idsensor': self.sensor_id,  # ID del sensor
            'valor': self.generate_realistic_value()  # Valor generado de aceleración
        }

        try:
            # Realiza una solicitud POST al endpoint de la API con los datos de lectura
            response = requests.post(f"{self.base_url}/api/sensor_data", json=reading)

            # Verifica el estado de la respuesta
            if response.status_code == 200:
                print(f"Lectura enviada correctamente: {reading}")
            else:
                # Si no es 200, muestra el código de estado y el mensaje de error
                print(f"Error al enviar la lectura. Código de estado: {response.status_code}, Respuesta: {response.text}")
        except requests.ConnectionError as e:
            # Captura y muestra errores de conexión
            print(f"Error de conexión: {e}")
        except Exception as e:
            # Captura y muestra cualquier otro tipo de error
            print(f"Error al enviar la lectura: {e}")

    def run(self):
        """
        Inicia la simulación del sensor, enviando lecturas periódicamente.
        """
        print(f"Iniciando simulación de sensor de aceleración para el sensor {self.sensor_id}")
        try:
            # Bucle infinito para enviar lecturas en intervalos definidos
            while True:
                self.send_reading()  # Envía una lectura
                time.sleep(self.interval)  # Espera el intervalo de tiempo definido antes de la siguiente lectura
        except KeyboardInterrupt:
            # Maneja una interrupción manual (Ctrl + C) para detener la simulación
            print("\nSimulación interrumpida manualmente. Saliendo...")
            sys.exit(0)  # Sale del programa limpiamente

# Bloque principal para ejecutar el script como programa independiente
if __name__ == "__main__":
    # Configuración inicial del simulador
    SENSOR_ID = "JCAO4275"  # ID del sensor, debe ser único
    API_URL = "http://localhost:5000"  # URL base de la API Flask donde se recibirán los datos
    INTERVAL = 30  # Intervalo entre lecturas en segundos

    # Crea una instancia del simulador con la configuración definida
    simulator = AccelerationSensorSimulator(SENSOR_ID, API_URL, INTERVAL)

    # Inicia la simulación del sensor
    simulator.run()
