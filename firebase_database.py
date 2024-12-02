# Importar las librerías necesarias de Firebase Admin SDK
import firebase_admin  # Librería principal para interactuar con Firebase
from firebase_admin import credentials, db  # Módulos específicos para autenticación y base de datos

# Definición de la clase para interactuar con la base de datos Firebase Realtime Database
class FirebaseDB:
    def __init__(self, credential_path, database_url):
        """
        Inicializa la conexión con Firebase Realtime Database.

        Args:
            credential_path (str): Ruta al archivo JSON con las credenciales del servicio Firebase.
            database_url (str): URL de la base de datos Realtime Database.
        """
        # Carga el archivo de credenciales del servicio
        cred = credentials.Certificate(credential_path)

        # Inicializa Firebase con las credenciales y el URL de la base de datos
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })

    def write_record(self, path, data):
        """
        Escribe un nuevo registro en la base de datos en la ubicación especificada.

        Args:
            path (str): Ruta en la base de datos donde se guardarán los datos.
            data (dict): Diccionario con los datos a guardar.
        """
        # Define una referencia al nodo especificado en la base de datos
        ref = db.reference(path)

        # Inserta un nuevo registro en el nodo, generando automáticamente un ID único
        ref.push(data)

    def read_record(self, path):
        """
        Lee todos los registros desde una ruta específica en la base de datos.

        Args:
            path (str): Ruta en la base de datos desde donde se leerán los datos.

        Returns:
            dict: Los datos leídos desde la base de datos.

        Raises:
            ValueError: Si no se encuentra ningún dato en la ruta especificada.
        """
        # Define una referencia al nodo especificado en la base de datos
        ref = db.reference(path)

        # Obtiene los datos desde la base de datos
        data = ref.get()

        # Verifica si se encontraron datos en la ruta especificada
        if data is None:
            raise ValueError(f"No data found at path: {path}")  # Lanza una excepción si no hay datos

        # Devuelve los datos obtenidos
        return data

    def update_record(self, path, data):
        """
        Actualiza un registro existente en la base de datos.

        Args:
            path (str): Ruta en la base de datos donde se encuentran los datos a actualizar.
            data (dict): Diccionario con los nuevos valores para actualizar.
        """
        # Define una referencia al nodo especificado en la base de datos
        ref = db.reference(path)

        # Actualiza los datos en la ruta especificada
        ref.update(data)

    def delete_record(self, path):
        """
        Elimina un registro o nodo completo en la base de datos.

        Args:
            path (str): Ruta en la base de datos donde se encuentran los datos a eliminar.
        """
        # Define una referencia al nodo especificado en la base de datos
        ref = db.reference(path)

        # Elimina los datos en la ruta especificada
        ref.delete()
