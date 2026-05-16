from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re
from logic import procesar_chat_whatsapp, obtener_ranking_mensajes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def es_formato_whatsapp_valido(texto: str) -> bool:
    """
    Valida formatos de Android e iOS.
    Ajustado para detectar AM/PM dentro y fuera de corchetes.
    """
    # Patrón Android: 10/5/24 20:30 - Nombre: ...
    patron_android = r'^\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?(\s*[ap]\.?\s?m\.?)?\s+-\s+'
    
    # Patrón iOS: [31/3/26, 6:45:17 p. m.] Nombre: ... (AM/PM dentro del corchete)
    patron_ios = r'^\[\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?(\s*[ap]\.?\s?m\.?)?\]\s+'

    lineas = texto.splitlines()
    # Revisamos las primeras 15 líneas para saltar mensajes de sistema si es necesario
    muestras = [l.strip() for l in lineas if l.strip()][:15]

    if not muestras:
        return False

    for linea in muestras:
        # Quitamos caracteres invisibles que a veces mete WhatsApp (como el LRM)
        linea_limpia = linea.encode('ascii', 'ignore').decode('ascii')
        if re.match(patron_android, linea) or re.match(patron_ios, linea):
            return True
            
    return False

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    print(f"--- Procesando: {file.filename} ---")

    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="El archivo debe ser .txt")

    contenido = await file.read()
    
    # Intentamos varias codificaciones por si el archivo viene de Windows o Mac
    for encoding in ["utf-8-sig", "utf-8", "latin-1"]:
        try:
            texto = contenido.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise HTTPException(status_code=400, detail="No se pudo leer el archivo.")

    if not es_formato_whatsapp_valido(texto):
        print("❌ Falló la validación de estructura.")
        raise HTTPException(
            status_code=400, 
            detail="El archivo no tiene el formato de chat de WhatsApp (revisá que sea el .txt exportado)."
        )

    print("✅ Archivo válido.")
    #dejo la funcion comentada por si necesitan corroborar algo del dataFrame
    #df_resultado = procesar_chat_whatsapp(texto) #el procesar_chat_whatsapp devuelve un dataframe con las columnas: Fecha, Hora, Miembro y Mensaje
    return {
        "nombre_archivo": file.filename,
        "lineas": len(texto.splitlines()),
        "mensaje": "¡Chat validado con éxito!",
        #"dataframe": df_resultado.to_dict(orient='records')  # Convertimos el DataFrame a una lista de diccionarios
    }
    
@app.post("/api/stats/top-senders")
async def top_senders(file: UploadFile = File(...)):
    contenido = await file.read()
    
    for encoding in ["utf-8-sig", "utf-8", "latin-1"]:
        try:
            texto = contenido.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise HTTPException(status_code=400, detail="No se pudo leer el archivo.")

    df = procesar_chat_whatsapp(texto)
    ranking = obtener_ranking_mensajes(df)
    
    return ranking.to_dict(orient='records')
