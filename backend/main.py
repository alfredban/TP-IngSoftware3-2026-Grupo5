from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File
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

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    contenido = await file.read()
    texto = contenido.decode("utf-8")
    
    return {
        "nombre_archivo": file.filename,
        "tamaño_bytes": len(contenido),
        "lineas": len(texto.splitlines()),
        "mensaje": "Archivo recibido correctamente"
    }