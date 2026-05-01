

CREATE TABLE canciones_artistas(
    cancion_id INTEGER REFERENCES canciones(cancion_id),
    artista_id INTEGER REFERENCES artistas(artista_id),
    PRIMARY KEY (cancion_id, artista_id)
);

CREATE TABLE canciones_generos(
    cancion_id INTEGER REFERENCES canciones(cancion_id),
    genero_id INTEGER REFERENCES generos(genero_id),
    PRIMARY KEY (cancion_id, genero_id)
);

CREATE TABLE canciones_productores(
    cancion_id INTEGER REFERENCES canciones(cancion_id),
    productor_id INTEGER REFERENCES productores(productor_id),
    PRIMARY KEY (cancion_id, productor_id)
);

CREATE TABLE playlist_canciones(
    playlist_id INTEGER REFERENCES playlists(playlist_id),
    cancion_id INTEGER REFERENCES canciones(cancion_id),
    PRIMARY KEY (playlist_id, cancion_id)
);