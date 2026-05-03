from db import get_connection
from extract import load_csv
from transform import (get_generos_unicos, get_artistas_unicos, get_albunes_unicos,
                       generar_productores, generar_usuarios, generar_playlist)
from load import (load_generos, load_artistas, load_albunes,
                  load_canciones, load_canciones_artistas, load_canciones_generos,
                  load_productores, load_usuarios, load_playlists,
                  load_canciones_productores, load_playlist_canciones)


def main():
    conn = get_connection()
    cursor = conn.cursor()
    print("Conexion exitosa a PostgreSQL")

    df = load_csv("data/dataset.csv")

    generos = get_generos_unicos(df)
    artistas = get_artistas_unicos(df)
    albunes = get_albunes_unicos(df)

    generos_dict = load_generos(cursor, generos)
    conn.commit()
    print(f"Generos insertados: {len(generos_dict)}")

    artistas_dict = load_artistas(cursor, artistas)
    conn.commit()
    print(f"Artistas insertados: {len(artistas_dict)}")

    albunes_dict = load_albunes(cursor, albunes, artistas_dict)
    conn.commit()
    print(f"Albunes insertados: {len(albunes_dict)}")

    canciones_dict = load_canciones(cursor, df, albunes_dict)
    conn.commit()
    print(f"Canciones insertadas: {len(canciones_dict)}")

    load_canciones_artistas(cursor, df, canciones_dict, artistas_dict)
    conn.commit()
    print("Relaciones canciones_artistas insertadas")

    load_canciones_generos(cursor, df, canciones_dict, generos_dict)
    conn.commit()
    print("Relaciones canciones_generos insertadas")

    productores = generar_productores(50)

    productores_dict = load_productores(cursor, productores)
    conn.commit()
    print(f"Productores insertados: {len(productores_dict)}")

    usuarios = generar_usuarios(100)
    usuarios_dict = load_usuarios(cursor, usuarios)
    conn.commit()
    print(f"Usuarios insertados: {len(usuarios_dict)}")

    playlists = generar_playlist(200)
    playlists_dict = load_playlists(cursor, playlists, usuarios_dict)
    conn.commit()
    print(f"Playlists insertadas: {len(playlists_dict)}")

    load_canciones_productores(cursor, canciones_dict, productores_dict)
    conn.commit()
    print("Relaciones canciones_productores insertadas")

    load_playlist_canciones(cursor, playlists_dict, canciones_dict)
    conn.commit()
    print("Relaciones playlist_canciones insertadas")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
