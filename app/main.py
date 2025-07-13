from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Hola desde EC2",
        "hora_utc": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }
