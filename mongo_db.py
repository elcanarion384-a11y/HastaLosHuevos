from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pydantic import BaseModel
from typing import Optional

# Conexión a MongoDB Atlas
MONGODB_URL = "mongodb+srv://elcanarion384_db_user:badc4c9a-6e77-4a90-a859-9b6e058a159e@cluster0.6zmczfd.mongodb.net/?appName=Cluster0"
MONGODB_DB = "hasta_los_huevos"

class Registro(BaseModel):
    """Modelo para validar datos de registro de sensores."""
    sensor: str
    valor: float
    unidad: str

def get_mongo_client():
    """Obtiene una conexión síncrona a MongoDB."""
    try:
        client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        # El ping asegura que la red permite la conexión
        client.admin.command('ping')
        return client
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"Error al conectar a MongoDB: {e}")
        raise

def get_db_collection(collection_name: str = "registros"):
    """Obtiene una colección de MongoDB."""
    client = get_mongo_client()
    db = client[MONGODB_DB]
    return db[collection_name]

def guardar_registro(registro_dict, collection_name="respuestas_test"):
    """Guarda un registro (diccionario) en MongoDB."""
    try:
        coleccion = get_db_collection(collection_name)
        resultado = coleccion.insert_one(registro_dict)
        print(f"✅ ID insertado en Atlas: {resultado.inserted_id}")
        return {"status": "guardado", "id": str(resultado.inserted_id)}
    except Exception as e:
        print(f"❌ Error en Mongo: {e}")
        return {"status": "error", "mensaje": str(e)}

def obtener_registros(collection_name: str = "registros", limite: int = 10) -> list:
    """Obtiene los últimos registros (Función síncrona)."""
    try:
        coleccion = get_db_collection(collection_name)
        registros = list(coleccion.find().sort("_id", -1).limit(limite))
        for reg in registros:
            reg["_id"] = str(reg["_id"])
        return registros
    except Exception as e:
        return {"error": str(e)}

def obtener_por_sensor(sensor: str, collection_name: str = "registros") -> list:
    """Filtra registros por sensor (Función síncrona)."""
    try:
        coleccion = get_db_collection(collection_name)
        registros = list(coleccion.find({"sensor": sensor}))
        for reg in registros:
            reg["_id"] = str(reg["_id"])
        return registros
    except Exception as e:
        return {"error": str(e)}
