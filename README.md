# AEMET - Recolector y Visor de Temperaturas

Este proyecto permite automatizar la descarga de datos meteorológicos desde la API oficial de AEMET y visualizarlos a través de un panel de control interactivo.

La configuración por defecto utiliza la estación **A Coruña (ID: 1387)**.

---

## Requisitos

- **Python 3.13** o superior.
- **API Key de AEMET**: Obtenible de forma gratuita en el [AEMET OpenData](https://opendata.aemet.es/).

---

## Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd aemetProyecto
   ```

2. **Instalar dependencias:**
   Se recomienda utilizar el archivo `requirements.txt` incluido para instalar todas las librerías necesarias (`requests`, `python-dotenv`, `streamlit`, `pandas`, `plotly`) de una sola vez:
   ```bash
   pip install -r requirements.txt
   ```

3. **Variables de entorno:**
   Crea un archivo llamado `.env` en la raíz del proyecto y añade tu clave:
   ```env
   API_KEY=tu_api_key_aquí
   ```

---

## Funcionamiento del Proyecto

El sistema se compone de dos módulos principales:

### 1. Extracción de Datos (`aemet.py`)
Este script descarga los datos de los últimos días y los almacena en una base de datos SQLite local.
- **Ejecución**: `python aemet.py`
- **Resultado**: Crea o actualiza el archivo `aemet_coruña.db`.

### 2. Visualización Interactiva (`graficas.py`)
Dashboard desarrollado con Streamlit que procesa la base de datos para mostrar:
- **Métricas principales**: Temperatura máxima absoluta, mínima y promedio del periodo.
- **Gráficos interactivos**: Comparativa de barras y líneas de tendencia mediante Plotly.
- **Explorador**: Acceso a la tabla completa de registros.
- **Ejecución**: `streamlit run graficas.py`

---

## Estructura de Datos (SQLite)

La información se organiza en la tabla `temperaturas` con el siguiente esquema:

| Columna    | Tipo    | Descripción                          |
|------------|---------|--------------------------------------|
| `id`       | INTEGER | Identificador único (Autoincremental) |
| `fecha`    | TEXT    | Fecha del registro (YYYY-MM-DD) |
| `estacion` | TEXT    | Identificador de la estación (ej. 1387) |
| `tmax`     | REAL    | Temperatura máxima diaria (°C) |

---

## Notas de Desarrollo
- **Manejo de Datos**: El sistema está preparado para procesar los datos en fragmentos (chunks) para optimizar la memoria [cite: 2026-03-04].
- **Gráficas**: Se recomienda usar el modo `x unified` en los gráficos de Plotly para una mejor lectura de las fechas.
