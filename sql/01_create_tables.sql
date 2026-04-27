

CREATE TABLE artistas (
    artista_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais VARCHAR(50)
);

CREATE TABLE albunes (
    album_id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    años_lanzamiento INTEGER,
    artista_id INTEGER REFERENCES artistas(artista_id) 
);

CREATE TABLE canciones (
    cancion_id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    duracion_segundos INTEGER,
    album_id INTEGER REFERENCE albunes(album_id)
);

CREATE TABLE generos (
    genero_id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE productores (
    productor_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais VARCHAR(50)
);

CREATE TABLE usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nombreusuario VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE playlists (
    playlist_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    usuario_id INTEGER REFERENCES usuarios(usuario_id)
);