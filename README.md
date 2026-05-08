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
│   ├── load_mongo.py                # Carga historial de reproducciones en MongoDB
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
├── dags/
│   └── pipeline_musica.py           # DAG: cargar_datos → cargar_mongo → dbt_run → dbt_test
├── Dockerfile.airflow               # Imagen personalizada con todas las dependencias
├── dbt_profiles.yml                 # Configuración de conexión dbt para Docker
├── tests/
├── logs/
├── docker-compose.yml               # PostgreSQL + MongoDB + Airflow
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

- [x] Agregar Airflow al docker-compose.yml (webserver + scheduler + airflow-db)
- [x] Crear imagen Docker personalizada con dependencias preinstaladas (`Dockerfile.airflow`)
- [x] Configurar `dbt_profiles.yml` para conexión dentro de la red Docker
- [x] Crear DAG `pipeline_musica`: `cargar_datos → dbt_run → dbt_test`
- [x] Pipeline corrió exitosamente: ETL ✓ — dbt run (7 modelos) ✓ — dbt test (10/10) ✓
- [x] Schedule `@daily` configurado — corre automáticamente cada día

### Fase 4 — MongoDB (historial de reproducciones)

- [x] Agregar MongoDB al docker-compose.yml
- [x] Crear `load_mongo.py` — genera 5000 eventos de reproducción con Faker
- [x] Integrar `cargar_mongo` al DAG de Airflow
- [x] Pipeline completo: cargar_datos → cargar_mongo → dbt_run → dbt_test ✓

### Fase 5 — Visualización con Metabase

- [x] Agregar Metabase al docker-compose.yml
- [x] Conectar Metabase a PostgreSQL
- [ ] Crear dashboards: top canciones, géneros más populares, artistas

> Los dashboards de Metabase quedaron pendientes. El proyecto se considera completo en su capa de ingeniería de datos (ETL, transformación, orquestación y almacenamiento híbrido). La visualización es un próximo paso.

---

## Cómo levantar el proyecto

```bash
# 1. Clonar el repo y crear el .env
cp .env.example .env

# 2. Construir imagen y levantar todos los servicios
docker-compose build
docker-compose up -d

# 3. Crear las tablas en PostgreSQL (primera vez)
psql -h localhost -p 5433 -U admin -d musicdb -f sql/01_create_tables.sql
psql -h localhost -p 5433 -U admin -d musicdb -f sql/02_create_pivot_tables.sql
psql -h localhost -p 5433 -U admin -d musicdb -f sql/03_alter_canciones.sql
psql -h localhost -p 5433 -U admin -d musicdb -f sql/04_add_constraints.sql

# 4. Triggerear el pipeline completo via API
curl -X POST "http://localhost:8080/api/v1/dags/pipeline_musica/dagRuns" \
  -H "Content-Type: application/json" \
  -u "admin:admin" \
  -d '{}'
```

Airflow UI disponible en `http://localhost:8080` (usuario: `admin`, password: `admin`).

El pipeline corre automáticamente cada día (`@daily`) y ejecuta:
1. ETL Python — carga datos desde CSV a PostgreSQL (Bronze)
2. `dbt run` — actualiza modelos staging y marts (Silver + Gold)
3. `dbt test` — valida calidad de datos (10 tests)

---

## Variables de entorno (.env.example)

```
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```
