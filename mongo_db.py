from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pydantic import BaseModel
from typing import Optional

# Conexión a MongoDB Atlas
MONGODB_URL = "mongodb+srv://elcanarion384_db_user:<db_password>@cluster0.6zmczfd.mongodb.net/?appName=Cluster0"
MONGODB_DB = "hasta_los_huevos"

class Registro(BaseModel):
    """Modelo para validar datos de registro de sensores."""
    sensor: str
    valor: float
    unidad: str

def get_mongo_client():
    """
    Obtiene una conexión a MongoDB.
    
    Returns:
        MongoClient: Cliente conectado a MongoDB
        
    Raises:
        ConnectionFailure: Si no se puede conectar a MongoDB
    """
    try:
        client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        return client
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"Error al conectar a MongoDB: {e}")
        raise

def get_db_collection(collection_name: str = "registros"):
    """
    Obtiene una colección de MongoDB.
    
    Args:
        collection_name (str): Nombre de la colección
        
    Returns:
        Collection: Colección de MongoDB
    """
    client = get_mongo_client()
    db = client[MONGODB_DB]
    return db[collection_name]

async def guardar_registro(registro: Registro, collection_name: str = "registros") -> dict:
    """
    Guarda un registro en MongoDB.
    
    Args:
        registro (Registro): Objeto registro con sensor, valor, unidad
        collection_name (str): Nombre de la colección
        
    Returns:
        dict: Resultado con el ID del documento insertado
    """
    try:
        coleccion = get_db_collection(collection_name)
        dato = registro.dict()
        resultado = coleccion.insert_one(dato)
        return {
            "status": "recibido",
            "id": str(resultado.inserted_id),
            "datos": dato
        }
    except Exception as e:
        return {
            "status": "error",
            "mensaje": str(e)
        }

async def obtener_registros(collection_name: str = "registros", limite: int = 10) -> list:
    """
    Obtiene los últimos registros de MongoDB.
    
    Args:
        collection_name (str): Nombre de la colección
        limite (int): Número máximo de registros a retornar
        
    Returns:
        list: Lista de registros
    """
    try:
        coleccion = get_db_collection(collection_name)
        registros = list(coleccion.find().sort("_id", -1).limit(limite))
        # Convertir ObjectId a string para serialización JSON
        for reg in registros:
            reg["_id"] = str(reg["_id"])
        return registros
    except Exception as e:
        return {"error": str(e)}

async def obtener_por_sensor(sensor: str, collection_name: str = "registros") -> list:
    """
    Obtiene registros filtrados por sensor.
    
    Args:
        sensor (str): Nombre del sensor a filtrar
        collection_name (str): Nombre de la colección
        
    Returns:
        list: Lista de registros del sensor especificado
    """
    try:
        coleccion = get_db_collection(collection_name)
        registros = list(coleccion.find({"sensor": sensor}))
        for reg in registros:
            reg["_id"] = str(reg["_id"])
        return registros
    except Exception as e:
        return {"error": str(e)}