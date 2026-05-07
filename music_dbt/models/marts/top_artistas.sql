select
    a.nombre as artista,
    round(avg(c.popularidad), 2) as popularidad_promedio,
    count(c.cancion_id) as total_canciones
from {{ref('stg_canciones')}} c
join public.canciones_artistas ca on c.cancion_id = ca.cancion_id
join {{ref('stg_artistas')}} a on ca.artista_id = a.artista_id
group by a.nombre
order by popularidad_promedio desc
limit 20