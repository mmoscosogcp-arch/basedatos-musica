from db import get_connection
from extract import load_csv
from transform import get_generos_unicos, get_artistas_unicos, get_albunes_unicos
from load import (load_generos, load_artistas, load_albunes,
                  load_canciones, load_canciones_artistas, load_canciones_generos)


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

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
