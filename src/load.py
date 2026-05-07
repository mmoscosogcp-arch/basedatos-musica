import pandas as pd
from transform import parse_artista
import random


def load_generos(cursor, generos: list) -> dict:
    generos_dict = {}
    for genero in generos:
        cursor.execute(
            "INSERT INTO generos (nombre) VALUES (%s) ON CONFLICT DO NOTHING", (genero,))

        cursor.execute(
            "SELECT genero_id FROM generos WHERE nombre = %s", (genero,)
        )
        resultado = cursor.fetchone()
        if resultado:
            generos_dict[genero] = resultado[0]

    return generos_dict


def load_artistas(cursor, artistas: set) -> dict:
    artista_dict = {}
    for artista in artistas:
        cursor.execute(
            "INSERT INTO artistas (nombre) VALUES (%s) ON CONFLICT DO NOTHING", (artista,))

        cursor.execute(
            "SELECT artista_id FROM artistas WHERE nombre = %s", (artista,)
        )
        resultado = cursor.fetchone()
        if resultado:
            artista_dict[artista] = resultado[0]

    return artista_dict


def load_albunes(cursor, albunes: pd.DataFrame, artistas_dict: dict) -> dict:
    albunes_dict = {}
    for _, fila in albunes.iterrows():
        albun = fila["album_name"]
        artista = parse_artista(fila["artists"])
        artista_id = artistas_dict.get(artista)
        if artista_id:
            cursor.execute(
                "INSERT INTO albunes (titulo, artista_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (
                    albun, artista_id)
            )

            cursor.execute(
                "SELECT album_id FROM albunes WHERE titulo = %s", (albun,)
            )

            resultado = cursor.fetchone()
            albunes_dict[albun] = resultado[0]

    return albunes_dict


def load_canciones(cursor, df: pd.DataFrame, albunes_dict: dict) -> dict:
    canciones_dict = {}
    for _, fila in df.iterrows():
        album = fila["album_name"]
        album_id = albunes_dict.get(album)
        if album_id:
            cursor.execute(
                """INSERT INTO canciones (titulo, duracion_segundos, album_id, popularidad, explicita,
                       danceability, energy, loudness, speechiness, acousticness,
                       instrumentalness, liveness, valence, tempo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING""", (fila["track_name"],
                                            int(fila["duration_ms"]),
                                            album_id,
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
            cursor.execute(
                "SELECT cancion_id FROM canciones WHERE titulo = %s", (
                    fila["track_name"],)
            )

            resultado = cursor.fetchone()
            if resultado:
                canciones_dict[fila["track_name"]] = resultado[0]

    return canciones_dict


def load_canciones_artistas(cursor, df: pd.DataFrame, canciones_dict: dict, artistas_dict: dict):
    for _, fila in df.iterrows():
        cancion = fila["track_name"]
        artista = parse_artista(fila["artists"])
        cancion_id = canciones_dict.get(cancion)
        artista_id = artistas_dict.get(artista)
        if cancion_id and artista_id:
            cursor.execute(
                "INSERT INTO canciones_artistas (cancion_id, artista_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (
                    cancion_id, artista_id)
            )


def load_canciones_generos(cursor, df: pd.DataFrame, canciones_dict: dict, generos_dict: dict):
    for _, fila in df.iterrows():
        cancion = fila["track_name"]
        genero = fila["track_genre"]
        cancion_id = canciones_dict.get(cancion)
        genero_id = generos_dict.get(genero)
        if cancion_id and genero_id:
            cursor.execute(
                "INSERT INTO canciones_generos (cancion_id, genero_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (
                    cancion_id, genero_id)
            )


def load_productores(cursor, productores: list) -> dict:
    productores_dict = {}
    for productor in productores:
        nombre = productor["nombre"][:5]
        pais = productor["pais"]
        if nombre:
            cursor.execute(
                "INSERT INTO productores (nombre, pais) VALUES (%s, %s) ON CONFLICT DO NOTHING", (
                    nombre, pais)
            )
            cursor.execute(
                "SELECT productor_id FROM productores WHERE nombre=%s", (
                    nombre,)
            )
            resultado = cursor.fetchone()
            if resultado:
                productores_dict[nombre] = resultado[0]

    return productores_dict


def load_usuarios(cursor, usuarios: list) -> dict:
    usuarios_dict = {}
    for usuario in usuarios:
        nombre_usuario = usuario["nombreusuario"]
        email_usuario = usuario["email"]
        if nombre_usuario:
            cursor.execute(
                "INSERT INTO usuarios (nombreusuario, email) VALUES (%s, %s) ON CONFLICT DO NOTHING", (
                    nombre_usuario, email_usuario)
            )
            cursor.execute(
                "SELECT usuario_id FROM usuarios WHERE nombreusuario=%s", (
                    nombre_usuario,)
            )
            resultado = cursor.fetchone()
            if resultado:
                usuarios_dict[nombre_usuario] = resultado[0]

    return usuarios_dict


def load_playlists(cursor, playlists: list, usuarios_dict: dict) -> dict:
    playlists_dict = {}
    for playlist in playlists:
        usuario_id = random.choice(list(usuarios_dict.values()))
        nombreplaylist = playlist["nombre"]
        if usuario_id:
            cursor.execute(
                "INSERT INTO playlists (nombre, usuario_id) VALUES (%s,%s) ON CONFLICT DO NOTHING", (
                    nombreplaylist, usuario_id)
            )
            cursor.execute(
                "SELECT playlist_id FROM playlists WHERE nombre=%s", (
                    nombreplaylist,)
            )
            resultado = cursor.fetchone()
            if resultado:
                playlists_dict[nombreplaylist] = resultado[0]

    return playlists_dict


def load_canciones_productores(cursor,  canciones_dict: dict, productores_id: dict):
    for clave, valor in canciones_dict.items():
        productor_id = random.choice(list(productores_id.values()))
        cancion_id = valor
        if productor_id:
            cursor.execute(
                "INSERT INTO canciones_productores (cancion_id, productor_id) VALUES (%s,%s) ON CONFLICT DO NOTHING", (
                    cancion_id, productor_id)
            )


def load_playlist_canciones(cursor, playlists_dict: dict, canciones_dict: dict):
    for clave, valor in playlists_dict.items():
        cancion_id = random.choice(list(canciones_dict.values()))
        playlist_id = valor
        if cancion_id:
            cursor.execute(
                "INSERT INTO playlist_canciones (playlist_id, cancion_id) VALUES (%s,%s) ON CONFLICT DO NOTHING", (
                    playlist_id, cancion_id)
            )
