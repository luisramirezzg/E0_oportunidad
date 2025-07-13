import paho.mqtt.client as mqtt
import os
import json
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Leer las variables de conexión desde .env
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
TOPIC = "stock/updates"
DATABASE_URL = os.getenv("DATABASE_URL")

# Conexión y escritura a la base de datos
def insert_stock(symbol, price, quantity, timestamp):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO stocks (symbol, price, quantity, timestamp)
        VALUES (%s, %s, %s, %s)
    """, (symbol, price, quantity, timestamp))
    conn.commit()
    cur.close()
    conn.close()

# Callback cuando se conecta al broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker MQTT con código: {rc}")
    client.subscribe(TOPIC)

# Callback cuando llega un mensaje
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        symbol = data["symbol"]
        price = float(data["price"])
        quantity = int(data["quantity"])
        timestamp = datetime.fromisoformat(data["timestamp"])

        insert_stock(symbol, price, quantity, timestamp)
        print(f"Guardado: {symbol} {price} {quantity} {timestamp}")
    except Exception as e:
        print("Error procesando mensaje:", e)

# Configuración del cliente MQTT
client = mqtt.Client()
client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Conexión al broker
client.connect(HOST, PORT, 60)
client.loop_forever()
