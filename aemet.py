import requests
import sqlite3
from datetime import datetime, timedelta
import urllib3
from dotenv import load_dotenv
import os

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://opendata.aemet.es/opendata/api"
ESTACION = "1387"  # A Coruña

# --- Fechas: último mes ---
hoy = datetime.today()
hace_un_mes = hoy - timedelta(days=32)

fecha_ini = hace_un_mes.strftime("%Y-%m-%dT00:00:00UTC")
fecha_fin = hoy.strftime("%Y-%m-%dT23:59:59UTC")

url = f"{BASE_URL}/valores/climatologicos/diarios/datos/fechaini/{fecha_ini}/fechafin/{fecha_fin}/estacion/{ESTACION}"

# --- Primera petición ---
print("Consultando AEMET...")
r = requests.get(url, params={"api_key": API_KEY}, verify=False)

print("Status code:", r.status_code)

if r.status_code != 200 or not r.text:
    print("❌ Error en la primera petición.")
    exit()

respuesta = r.json()

if respuesta.get("estado") != 200:
    print("❌ AEMET devolvió error:", respuesta.get("descripcion"))
    exit()

# --- Segunda petición: datos reales ---
print("Obteniendo datos...")
datos = requests.get(respuesta["datos"], params={"api_key": API_KEY}, verify=False).json()

if not datos:
    print("❌ No se obtuvieron datos.")
    exit()

print(f"✅ {len(datos)} días recibidos.")

# --- Crear base de datos SQLite ---
conn = sqlite3.connect("aemet_coruña.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS temperaturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        estacion TEXT NOT NULL,
        tmax REAL
    )
""")

# --- Insertar datos ---
for dia in datos:
    fecha = dia.get("fecha")
    tmax = dia.get("tmax", None)

    if tmax:
        tmax = float(tmax.replace(",", "."))

    cursor.execute("""
        INSERT INTO temperaturas (fecha, estacion, tmax)
        VALUES (?, ?, ?)
    """, (fecha, ESTACION, tmax))

conn.commit()
conn.close()

print(f"✅ Base de datos 'aemet_coruña.db' creada con {len(datos)} registros.")