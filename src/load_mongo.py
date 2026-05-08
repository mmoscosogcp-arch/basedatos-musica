import random
from datetime import datetime, timedelta
from faker import Faker
from pymongo import MongoClient
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

fake = Faker()


def get_ids_from_postgres():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    cursor = conn.cursor()

    cursor.execute("SELECT cancion_id FROM canciones LIMIT 500")
    cancion_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT usuario_id FROM usuarios")
    usuario_ids = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return cancion_ids, usuario_ids


def generar_reproducciones(cancion_ids, usuario_ids, n=5000):
    reproducciones = []
    dispositivos = ["mobile", "desktop", "tablet", "smart_tv"]

    for _ in range(n):
        fecha = fake.date_time_between(start_date="-6m", end_date="now")
        reproducciones.append({
            "usuario_id": random.choice(usuario_ids),
            "cancion_id": random.choice(cancion_ids),
            "fecha": fecha,
            "dispositivo": random.choice(dispositivos),
            "duracion_escuchada_seg": random.randint(10, 300),
            "completa": random.choice([True, False])
        })

    return reproducciones


def load_mongo(reproducciones):
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    client = MongoClient(f"mongodb://{mongo_host}:27017/")
    db = client["musicdb"]
    coleccion = db["reproducciones"]
    coleccion.delete_many({})
    coleccion.insert_many(reproducciones)
    print(f"{len(reproducciones)} reproducciones insertadas en MongoDB")
    client.close()


if __name__ == "__main__":
    cancion_ids, usuario_ids = get_ids_from_postgres()
    reproducciones = generar_reproducciones(cancion_ids, usuario_ids)
    load_mongo(reproducciones)
