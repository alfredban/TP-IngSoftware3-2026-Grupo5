from collections import Counter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import emoji 
import numpy as np
import datetime as dt
import re
from stopwords import STOP_WORDS_ES # Importamos nuestra lista de palabras vacías

def IniciaConFechaYHora(s):
    s_limpio = s.encode('ascii', 'ignore').decode('ascii')
    patron_android = r'^\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?(\s*[ap]\.?\s?m\.?)?\s+-\s+'
    patron_ios = r'^\[\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?(\s*[ap]\.?\s?m\.?)?\]\s+'
    if re.match(patron_android, s_limpio) or re.match(patron_ios, s_limpio):
        return True
    return False

def EncontrarMiembro(s):
    return ': ' in s

def ObtenerPartes(linea):
    linea_limpia = linea.replace('\u200e', '').replace('\u200f', '')
    es_ios = linea_limpia.startswith('[')
    
    try:
        if es_ios:
            splitLinea = linea_limpia.split('] ', 1)
            FechaHora = splitLinea[0].replace('[', '')
            MensajeCompleto = splitLinea[1]
            
            if ', ' in FechaHora:
                Fecha, Hora = FechaHora.split(', ', 1)
            else:
                Fecha, Hora = FechaHora.split(' ', 1)
        else:
            splitLinea = linea_limpia.split(' - ', 1)
            FechaHora = splitLinea[0]
            MensajeCompleto = splitLinea[1]
            Fecha, Hora = FechaHora.split(' ', 1)

        if EncontrarMiembro(MensajeCompleto): 
            splitMensaje = MensajeCompleto.split(': ', 1)      
            Miembro = splitMensaje[0]                 
            Mensaje = splitMensaje[1]      
        else:
            Miembro = None
            Mensaje = MensajeCompleto
            
        return Fecha, Hora, Miembro, Mensaje
    except Exception:
        return None, None, None, linea

def procesar_chat_whatsapp(texto_completo):
    DatosLista = []
    lineas = texto_completo.splitlines()
    
    # Saltamos la primera línea (cifrado extremo a extremo)
    if len(lineas) > 0:
        lineas = lineas[1:]
        
    VerificarMensaje = []
    Fecha, Hora, Miembro = None, None, None
    
    for linea in lineas:
        linea = linea.strip()
        if not linea: continue
        
        if IniciaConFechaYHora(linea):
            # Si ya veníamos acumulando un mensaje anterior, lo guardamos
            if len(VerificarMensaje) > 0:
                DatosLista.append([Fecha, Hora, Miembro, ' '.join(VerificarMensaje)])
            
            # Limpiamos para el nuevo mensaje
            VerificarMensaje.clear()
            # Obtenemos las partes del nuevo mensaje
            Fecha, Hora, Miembro, Mensaje = ObtenerPartes(linea)
            VerificarMensaje.append(Mensaje)
        else:
            # Es un salto de línea del mensaje anterior
            VerificarMensaje.append(linea)
            
    # verificamos el último mensaje del archivo
    if len(VerificarMensaje) > 0:
        DatosLista.append([Fecha, Hora, Miembro, ' '.join(VerificarMensaje)])
        
    # Crear DataFrame
    df = pd.DataFrame(DatosLista, columns=['Fecha', 'Hora', 'Miembro', 'Mensaje'])
    
    # Limpieza de datos
    df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
    df['Fecha'] = df['Fecha'].dt.strftime('%d/%m/%Y')
    df = df.dropna()
    df.reset_index(drop=True, inplace=True)
    
    return df

def obtener_ranking_mensajes(df):
    # Filtramos los mensajes del sistema (Miembro = None o mensajes automáticos)
    df_filtrado = df[df['Miembro'].notna()].copy()
    
    # Se cuentan los mensajes de cada miembro
    conteo = df_filtrado['Miembro'].value_counts().reset_index()
    conteo.columns = ['miembro', 'cantidad_mensajes']
    
    return conteo

def emogiMasUsado(df:pd.DataFrame, texto:str ="Mensaje"):
    all_emojis = []     #lista para guardar todos los emojis del dataframe
    for mensaje in df[texto].dropna().astype(str):
        for em in emoji.analyze(mensaje):
            all_emojis.append(em.chars)

    if not all_emojis:
        return {"emoji": None, "cantidad": 0}
    
    contador = Counter(all_emojis)  # Contamos la frecuencia de cada emoji
    masUsado = contador.most_common(1)[0]  # Devuelve una tupla (emoji, cantidad)

    return {"emoji": masUsado[0], "cantidad": masUsado[1]}

def obtener_mensajes_por_hora(df: pd.DataFrame):
    if df.empty:
        # CORRECCIÓN: Ahora devolvemos el entero i en lugar de f"{i}h"
        return [{"hour": i, "messages": 0} for i in range(24)]
    
    df_copy = df.copy()
    
    # Función auxiliar para convertir la hora a formato 24hs
    def extraer_hora(hora_str):
        hora_str = str(hora_str).lower()
        match = re.search(r'(\d{1,2}):\d{2}', hora_str)
        if not match:
            return 0
        h = int(match.group(1))
        if 'p' in hora_str and 'm' in hora_str:
            if h < 12:
                h += 12
        elif 'a' in hora_str and 'm' in hora_str:
            if h == 12:
                h = 0
        return h
    
    # Aplica la función para obtener la hora en formato 24hs
    df_copy['hour_24'] = df_copy['Hora'].apply(extraer_hora)
    
    # Obtener la cantidad de días únicos en los que hubo mensajes
    dias_unicos = df_copy['Fecha'].nunique()
    if dias_unicos == 0:
        dias_unicos = 1

    # Contar la cantidad de mensajes que se enviaron en cada hora a nivel general
    conteo_por_hora = df_copy.groupby('hour_24').size()

    # Array de 24 elementos (uno por cada hora del día)
    resultado = []
    for i in range(24):
        total_mensajes = conteo_por_hora.get(i,0)
        promedio = round(total_mensajes / dias_unicos)
        # CORRECCIÓN: "hour" ahora es integer puro
        resultado.append({"hour": i, "messages": int(promedio)})
    
    return resultado

def obtener_mensajes_por_dia_semana(df: pd.DataFrame):
    dias_orden = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    resultado_base = {dia: 0 for dia in dias_orden}
    
    if not df.empty:
        df_filtrado = df[df['Miembro'].notna()].copy()
        
        if not df_filtrado.empty:
            df_filtrado['Fecha_dt'] = pd.to_datetime(df_filtrado['Fecha'], dayfirst=True, errors='coerce')
            
            dias_es = {0: 'Lunes', 1: 'Martes', 2: 'Miercoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'}
            df_filtrado['dia_semana'] = df_filtrado['Fecha_dt'].dt.dayofweek.map(dias_es)
            
            conteo = df_filtrado.groupby('dia_semana').size()
            
            semanas_unicas = df_filtrado['Fecha_dt'].dt.isocalendar().week.nunique()
            if semanas_unicas == 0:
                semanas_unicas = 1
                
            for dia, cantidad in conteo.items():
                if dia in resultado_base:
                    resultado_base[dia] = int(round(cantidad / semanas_unicas))
                
    resultado = [{"day": dia, "messages": cantidad} for dia, cantidad in resultado_base.items()]
    
    return resultado

def obtener_frecuencia_palabras(df, limite_palabras: int = 50):
    # Toma un DataFrame con los datos de Whatsapp, extrae los mensajes, limia el texto,
    # filtra las stopwords y devuelve un array con el top `limite_palabras` mas usadas

    # Unir todos los mensajes en un solo string gigante
    todos_los_mensajes = " ".join (df['Mensaje'].astype(str).to_list())

    # Convertir a minúsculas
    texto_limpio = todos_los_mensajes.lower()

    # Eliminar URLs
    texto_limpio = re.sub(r'https?://\S+|www\.\S+', '', texto_limpio)

    # Eliminar menciones
    texto_limpio = re.sub(r'@\w+', '', texto_limpio)

    # Extraer solo palabras estrictamente alfabéticas (elimina: emojis, números, símbolos y guiones bajos)
    palabras = re.findall(r'[^\W\d_]+', texto_limpio)

    # Filtrar las palabras que estan incluidas en el archivo stopwords.py
    palabras_filtradas = [p for p in palabras if p not in STOP_WORDS_ES and len(p)>2]

    # Contar la frecuencia de cada palabra
    contador_palabras = Counter(palabras_filtradas)

    # Obtener las palabras mas usadas
    top_palabras = contador_palabras.most_common(limite_palabras)

    # Formatear la respuesta
    worldcloud_data = [
        {"word": palabra, "frecuency": frecuencia} for palabra, frecuencia in top_palabras
    ]

    return worldcloud_data