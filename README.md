# AEMET - Recolector de Temperaturas

Script Python que consulta la API pública de AEMET (Agencia Estatal de Meteorología) y almacena los datos de temperatura máxima de los últimos 32 días en una base de datos SQLite local.

La estación meteorológica configurada por defecto es **A Coruña (ID: 1387)**.

---

## Requisitos

- Python 3.8 o superior
- Conexión a internet
- API Key de AEMET (gratuita, ver instrucciones abajo)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd aemetProyecto
```

### 2. Instalar dependencias

```bash
pip install requests python-dotenv
```

### 3. Obtener una API Key de AEMET

1. Accede a [https://opendata.aemet.es/centrodedescargas/inicio](https://opendata.aemet.es/centrodedescargas/inicio)
2. Haz clic en **"Obtener API Key"**
3. Introduce tu correo electrónico y acepta las condiciones
4. Recibirás la API Key por email en unos minutos

### 4. Configurar las credenciales

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
API_KEY=tu_api_key_aqui
```

> El archivo `.env` está incluido en `.gitignore` y nunca se subirá al repositorio.

---

## Uso

Ejecuta el script desde la terminal:

```bash
python aemet.py
```

### Salida esperada

```
Consultando AEMET...
Status code: 200
Obteniendo datos...
✅ 32 días recibidos.
✅ Base de datos 'aemet_coruña.db' creada con 32 registros.
```

Tras la ejecución se generará (o actualizará) el archivo `aemet_coruña.db` en el directorio actual.

---

## Base de datos

Los datos se almacenan en SQLite en la tabla `temperaturas`:

| Columna   | Tipo    | Descripción                         |
|-----------|---------|-------------------------------------|
| `id`      | INTEGER | Clave primaria autoincremental      |
| `fecha`   | TEXT    | Fecha del registro (YYYY-MM-DD)     |
| `estacion`| TEXT    | ID de la estación AEMET             |
| `tmax`    | REAL    | Temperatura máxima del día (°C)     |

Para consultar los datos puedes usar cualquier cliente SQLite o Python:

```python
import sqlite3
conn = sqlite3.connect("aemet_coruña.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM temperaturas ORDER BY fecha DESC LIMIT 10")
print(cursor.fetchall())
conn.close()
```

---

## Cambiar la estación meteorológica

Edita la variable `ESTACION` en [aemet.py](aemet.py) con el ID de la estación que desees:

```python
ESTACION = "1387"  # A Coruña — cambia este valor
```

Puedes buscar el ID de tu estación en el [catálogo de estaciones de AEMET](https://opendata.aemet.es/centrodedescargas/productosAEMET).
