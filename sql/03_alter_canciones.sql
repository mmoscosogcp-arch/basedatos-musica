
ALTER TABLE canciones
ADD COLUMN popularidad INTEGER,
ADD COLUMN explicita BOOLEAN,
ADD COLUMN danceability FLOAT,
ADD COLUMN energy FLOAT,
ADD COLUMN loudness FLOAT,
ADD COLUMN speechiness FLOAT,
ADD COLUMN acousticness FLOAT,
ADD COLUMN instrumentalness FLOAT,
ADD COLUMN liveness FLOAT,
ADD COLUMN valence FLOAT,
ADD COLUMN tempo FLOAT;

