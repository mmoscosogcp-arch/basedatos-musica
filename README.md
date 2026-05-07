# Music Database — Proyecto Data Engineering

Pipeline completo de datos musicales usando Python, PostgreSQL, dbt, Airflow y Metabase, todo orquestado con Docker.

---

## Objetivo

Aprender el flujo completo de Data Engineering: ingesta, transformación, orquestación, calidad de datos y visualización, usando un dataset real de canciones de Spotify.

## Stack tecnológico

| Herramienta        | Rol                                    |
| ------------------ | -------------------------------------- |
| Python             | Scripts de ingesta y transformación    |
| PostgreSQL 15      | Base de datos relacional               |
| Docker Compose     | Orquestación de servicios              |
| dbt                | Transformaciones y modelos analíticos  |
| Apache Airflow     | Orquestación y scheduling de pipelines |
| Great Expectations | Validación y calidad de datos          |
| Metabase           | Visualización y dashboards             |
| Faker              | Generación de datos ficticios          |

---

## Arquitectura — Medallion

```
Bronze (crudo)          Silver (staging/dbt)       Gold (marts/dbt)
────────────────────    ──────────────────────     ──────────────────────────
canciones          →    stg_canciones         →    top_artistas_populares
artistas           →    stg_artistas          →    generos_mas_escuchados
generos            →    stg_generos           →    canciones_por_energia
(PostgreSQL)            (vistas limpias)           (tablas analíticas)
```

## Estructura del proyecto

```
basedatos-musica/
├── data/
│   └── dataset.csv                  # Dataset Spotify
├── src/
│   ├── db.py
│   ├── extract.py
│   ├── load.py
│   ├── main.py
│   └── transform.py
├── sql/
│   ├── 01_create_tables.sql         # Tablas principales
│   ├── 02_create_pivot_tables.sql   # Tablas pivote (N:M)
│   ├── 03_alter_canciones.sql       # Columnas adicionales
│   └── 04_add_constraints.sql       # Constraints UNIQUE
├── music_dbt/                       # Proyecto dbt (Fase 2)
│   ├── models/
│   │   ├── staging/                 # Capa Silver: limpieza de tablas crudas
│   │   │   ├── stg_canciones.sql
│   │   │   ├── stg_artistas.sql
│   │   │   └── stg_generos.sql
│   │   └── marts/                   # Capa Gold: modelos analíticos
│   └── dbt_project.yml
├── dags/                            # (Fase 3 — Airflow)
├── tests/
├── logs/
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── .env                             # No se sube a GitHub
```

---

## Modelo de datos

```
artistas ──< albunes ──< canciones >── canciones_generos ──> generos
                              │
                              ├──< canciones_artistas >── artistas
                              └──< canciones_productores >── productores

usuarios ──< playlists >── playlist_canciones >── canciones
```

---

## Roadmap

### Fase 1 — Carga de datos (ETL básico)

- [x] Crear tablas en PostgreSQL
- [x] Cargar géneros, artistas, álbumes, canciones desde CSV
- [x] Cargar tabla pivote `canciones_artistas`
- [x] Cargar tabla pivote `canciones_generos`
- [x] Generar datos ficticios para `productores`, `usuarios`, `playlists` con Faker
- [x] Cargar tablas pivote `canciones_productores` y `playlist_canciones`

### Fase 2 — Transformaciones con dbt

- [x] Instalar y configurar dbt-postgres (Python 3.11)
- [x] Conectar dbt a PostgreSQL (`dbt debug` exitoso)
- [x] Crear modelos staging: `stg_canciones`, `stg_artistas`, `stg_generos`, `stg_albunes`
- [x] Crear modelos marts: `top_artistas`, `generos_populares`, `canciones_audio_features`
- [x] Documentar modelos con `schema.yml` (tests: unique, not_null)
- [x] Correr `dbt run` — vistas creadas en PostgreSQL
- [x] Correr `dbt test` — 10/10 tests pasaron

### Fase 3 — Orquestación con Airflow

- [ ] Agregar Airflow al docker-compose.yml
- [ ] Convertir load_data.py en DAG de Airflow
- [ ] Crear DAG para ejecutar modelos dbt
- [ ] Programar ejecución automática del pipeline completo

### Fase 4 — Calidad de datos

- [ ] Agregar validaciones con Great Expectations
- [ ] Validar nulos, duplicados y rangos en columnas críticas
- [ ] Generar reporte de calidad automático en cada ejecución

### Fase 5 — Visualización con Metabase

- [ ] Agregar Metabase al docker-compose.yml
- [ ] Conectar Metabase a PostgreSQL
- [ ] Crear dashboards: top canciones, géneros más populares, artistas

---

## Cómo levantar el proyecto

```bash
# 1. Clonar el repo y crear el .env
cp .env.example .env

# 2. Levantar PostgreSQL
docker-compose up -d

# 3. Crear las tablas
psql -h localhost -p 5433 -U admin -d musicdb -f sql/01_create_tables.sql
psql -h localhost -p 5433 -U admin -d musicdb -f sql/02_create_pivot_tables.sql
psql -h localhost -p 5433 -U admin -d musicdb -f sql/03_alter_canciones.sql
psql -h localhost -p 5433 -U admin -d musicdb -f sql/04_add_constraints.sql

# 4. Cargar datos (Bronze layer)
source venv/bin/activate
cd src && python main.py

# 5. Correr transformaciones dbt (Silver + Gold layer)
source venv_dbt/bin/activate
cd music_dbt
dbt run

# 6. Validar calidad de datos
dbt test
```

---

## Variables de entorno (.env.example)

```
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```
