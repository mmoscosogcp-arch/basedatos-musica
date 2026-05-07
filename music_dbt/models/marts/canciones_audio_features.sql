select
    c.titulo,
    a.nombre as artista,
    c.popularidad,
    c.danceability,
    c.energy,
    c.tempo,
    c.valence,
    case
        when c.danceability >= 0.7 then 'alta'
        when c.danceability >= 0.4 then 'media'
        else 'baja'
    end as nivel_danceability,
    case
        when c.energy >= 0.7 then 'alta'
        when c.energy >= 0.4 then 'media'
        else 'baja'
    end as nivel_energy
from {{ref ('stg_canciones')}} c
join public.canciones_artistas ca on c.cancion_id = ca.cancion_id
join {{ref('stg_artistas')}} a on ca.artista_id = a.artista_id
order by c.popularidad desc
limit 100