select 
    g.nombre as genero,
    count(c.cancion_id) as total_canciones,
    round(avg(c.popularidad),2) as popularidad_promedio
from {{ref('stg_generos')}} g
join public.canciones_generos cg on g.genero_id = cg.genero_id
join {{ref('stg_canciones')}} c on cg.cancion_id = c.cancion_id
group by g.nombre
order by total_canciones desc