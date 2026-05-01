import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os
import ast
import warnings
warnings.filterwarnings("ignore")

load_dotenv()


conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()
print("Conexion exitosa a PostgreSQL")


df = pd.read_csv("data/dataset.csv")
df = df.dropna(subset=["artists", "artists", "track_name"])
df["duration_ms"] = (df["duration_ms"] / 1000).astype(int)

generos = df["track_genre"].drop_duplicates().dropna()
for genero in generos:
    cursor.execute(
        "INSERT INTO generos (nombre) VALUES (%s) ON CONFLICT DO NOTHING", (genero,)
    )
conn.commit()
print(f"Generos insertados: {len(generos)}")


artistas_unicos = set()
for valor in df["artists"].dropna():
    try:
        lista = ast.literal_eval(valor)
        for artista in lista:
            artistas_unicos.add(artista.strip())
    except:
        for artista in valor.split(";"):
            artistas_unicos.add(artista.strip())


for artista in artistas_unicos:
    cursor.execute(
        "INSERT INTO artistas (nombre) VALUES (%s) ON CONFLICT DO NOTHING", (artista,)
    )
conn.commit()
print(f"Artistas insertados: {len(artistas_unicos)}")


albunes_unicos = df[["album_name", "artists"]].drop_duplicates(subset=[
    "album_name"])

for _, fila in albunes_unicos.iterrows():
    try:
        lista = ast.literal_eval(fila["artists"])
        artista_nombre = lista[0].strip()
    except:
        artista_nombre = fila["artists"].split(";")[0].strip()

    cursor.execute(
        "SELECT artista_id FROM artistas WHERE nombre = %s", (artista_nombre,))
    resultado = cursor.fetchone()
    if resultado:
        cursor.execute(
            "INSERT INTO albunes (titulo, artista_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (fila["album_name"], resultado[0])
        )
conn.commit()
print(f"albunes insertados: {len(albunes_unicos)}")

for _, fila in df.iterrows():
    cursor.execute(
        "SELECT album_id FROM albunes WHERE titulo = %s", (fila["album_name"],))
    resultado = cursor.fetchone()
    if resultado:
        cursor.execute("""
            INSERT INTO canciones (titulo, duracion_segundos, album_id, popularidad, explicita,
                       danceability, energy, loudness, speechiness, acousticness,
                       instrumentalness, liveness, valence, tempo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING""",
                       (fila["track_name"],
                        int(fila["duration_ms"]),
                           resultado[0],
                           int(fila["popularity"]),
                           bool(fila["explicit"]),
                           fila["danceability"],
                           fila["energy"],
                           fila["loudness"],
                           fila["speechiness"],
                           fila["acousticness"],
                           fila["instrumentalness"],
                           fila["liveness"],
                           fila["valence"],
                           fila["tempo"]
                        ))


conn.commit()
print(f"Canciones insertados: {len(df)}")
