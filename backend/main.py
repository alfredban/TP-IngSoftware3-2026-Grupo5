from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Esto permite que tu React (puerto 5173) lea los datos del Back (puerto 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Backend funcionando correctamente"}

@app.get("/api/test")
def test():
    return {"mensaje": "¡Conexión exitosa desde el servidor!"}