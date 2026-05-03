
ALTER TABLE generos ADD CONSTRAINT uq_generos_nombre UNIQUE (nombre);
ALTER TABLE artistas ADD CONSTRAINT uq_artistas_nombre UNIQUE (nombre);
ALTER TABLE albunes ADD CONSTRAINT uq_albunes_titulo UNIQUE (titulo);
ALTER TABLE canciones ADD CONSTRAINT uq_canciones_titulo_album UNIQUE (titulo, album_id);
