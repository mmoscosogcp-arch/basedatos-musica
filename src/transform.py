import ast
import pandas as pd
from faker import Faker

fake = Faker()


def get_generos_unicos(df: pd.DataFrame) -> list:
    generos = df["track_genre"].drop_duplicates().dropna()

    return generos


def get_artistas_unicos(df: pd.DataFrame) -> set:
    artistas_unicos = set()
    for valores in df["artists"].dropna():
        try:
            lista = ast.literal_eval(valores)
            for artista in lista:
                artistas_unicos.add(artista.strip())
        except:
            for artista in valores.split(";"):
                artistas_unicos.add(artista.strip())

    return artistas_unicos


def get_albunes_unicos(df: pd.DataFrame) -> pd.DataFrame:
    albunes_unicos = df[["album_name", "artists"]
                        ].drop_duplicates(subset=["album_name"])

    return albunes_unicos


def parse_artista(valor: str) -> str:
    try:
        lista_artista = ast.literal_eval(valor)
        return lista_artista[0].strip()
    except:
        return valor.split(";")[0].strip()


def generar_productores(n: int) -> list:
    productores = []
    for _ in range(n):
        productores.append(
            {"nombre": fake.unique.name(), "pais": fake.country()})
    return productores


def generar_usuarios(n: int) -> list:
    usuarios = []
    for _ in range(n):
        usuarios.append(
            {"nombreusuario": fake.unique.user_name(), "email": fake.email()})
    return usuarios


def generar_playlist(n: int) -> list:
    playlists = []
    for _ in range(n):
        playlists.append({"nombre":  fake.catch_phrase()})
    return playlists
