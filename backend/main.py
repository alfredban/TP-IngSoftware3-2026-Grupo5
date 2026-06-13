from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import re
from logic import (
    procesar_chat_whatsapp, 
    obtener_ranking_mensajes, 
    emogiMasUsado, 
    obtener_mensajes_por_hora, 
    obtener_mensajes_por_dia_semana, 
    obtener_frecuencia_palabras
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generar_respuesta_error(error_nombre: str, info_detalle: str, status: int = 400):
    return JSONResponse(
        status_code=status,
        content={
            "filename": "",
            "file_size": 0,
            "file_type": "",
            "metrics": {},
            "errors": [{"error": error_nombre, "info": info_detalle}]
        }
    )

def es_formato_whatsapp_valido(texto: str) -> bool:
    patron_android = r'^\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?(\s*[ap]\.?\s?m\.?)?\s+-\s+'
    patron_ios = r'^\[\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?(\s*[ap]\.?\s?m\.?)?\]\s+'

    lineas = texto.splitlines()
    muestras = [l.strip() for l in lineas if l.strip()][:15]

    if not muestras:
        return False

    for linea in muestras:
        linea_limpia = linea.encode('ascii', 'ignore').decode('ascii')
        if re.match(patron_android, linea) or re.match(patron_ios, linea):
            return True
            
    return False

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    print(f"--- Procesando: {file.filename} ---")

    if not file.filename.endswith('.txt'):
        return generar_respuesta_error("Formato inválido", "El archivo debe ser .txt")

    contenido = await file.read()
    
    for encoding in ["utf-8-sig", "utf-8", "latin-1"]:
        try:
            texto = contenido.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        return generar_respuesta_error("Error de lectura", "No se pudo leer la codificación del archivo.")

    if not es_formato_whatsapp_valido(texto):
        return generar_respuesta_error(
            "Formato incorrecto", 
            "El archivo no tiene el formato de chat de WhatsApp (revisá que sea el .txt exportado)."
        )

    try:
        df = procesar_chat_whatsapp(texto)
        
        # 1. Total de mensajes (filtrando nulos del sistema)
        total_mensajes = len(df[df['Miembro'].notna()])
        
        # 2. Usuario que más mensajes envió
        ranking_mensajes = obtener_ranking_mensajes(df)
        top_sender = ranking_mensajes.iloc[0]['miembro'] if not ranking_mensajes.empty else ""
        
        # 3. Emoji más utilizado
        emoji_data = emogiMasUsado(df)
        top_emoji = emoji_data['emoji'] if emoji_data['emoji'] else ""
        
        # 4. Franja horaria con mayor actividad
        messages_by_hour = obtener_mensajes_por_hora(df)
        
        # 5. Días con mayor cantidad de mensajes
        messages_by_day_of_week = obtener_mensajes_por_dia_semana(df)
        
        # 6. Nube de palabras
        wordcloud_data = obtener_frecuencia_palabras(df)

        return {
            "filename": file.filename,
            "file_size": len(contenido),
            "file_type": "txt",
            "metrics": {
                "total_messages": total_mensajes,
                "top_sender": top_sender,
                "top_emoji": top_emoji,
                "messages_by_hour": messages_by_hour,
                "messages_by_day_of_week": messages_by_day_of_week,
                "wordcloud_data": wordcloud_data
            },
            "errors": []
        }

    except Exception as e:
        return generar_respuesta_error("Error interno del servidor", str(e), status=500)