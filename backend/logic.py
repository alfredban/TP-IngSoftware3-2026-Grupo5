from collections import Counter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import emoji 
import numpy as np
import datetime as dt
import re

 ##verifica el macht con el patron de fecha y hora al inicio de cada linea del txt 
def IniciaConFechaYHora(s):
    
    patrones = [
                r'^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4},?\s[0-9]{1,2}:[0-9]{2}\s-', #10/4/2026, 18:37 -
                r'^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4},?\s[0-9]{1,2}:[0-9]{2}\s[ap]\.?\s?m\.?\s-' #31/3/2026, 7:17 p. m. - 
            ]                                     
    
    patron = '|'.join(patrones)
    resultado = re.match(patron, s, re.IGNORECASE)
    if resultado:
        return True
    return False
  
# Patron para encontrar a los miembros del grupo dentro del txt
def EncontrarMiembro(s):
    patrones = [
        r'([\w]+):',                                 # Nombre
        r'([\w]+[\s]+[\(]+[\w]+[\)]+):',             # Nombre (Apodo)
        r'([\w]+[\s]+[\w]+):',                       # Nombre + Apellido
        r'([\w]+[\s]+[\w]+[\s]+[\w]+):',             # Nombre 1 + Nombre 2 + Apellido
        r'([+]\d{1,3}[\s\d\-\(\)]{8,15}):',          # Número de teléfono (en teoria deberia de cubrir almenos latinoamerica)
        r'([\w]+)[\u263a-\U0001f999]+:',             # Nombre + Emoji            
    ]
    patron = '^' + '|'.join(patrones)     
    resultado = re.match(patron, s)  # Verificar si cada línea del txt hace match con el patrón de miembro
    if resultado:
        return True
    return False
  

# split [0] = todo a la izquierda del primer guion, split [1] = todo a la derecha del primer guion
# basicamente vamos partiendo la linea en partes, primero por el guion, luego por el espacio, luego por los dos puntos,
# etc. para obtener cada parte de la linea del txt
# Separar las partes de cada línea del txt: Fecha, Hora, Miembro y Mensaje
def ObtenerPartes(linea):   
    # Ejemplo: '21/2/2021 11:27 a. m. - Sandro: Todos debemos aprender a analizar datos'
    splitLinea = linea.split(' - ') 
    FechaHora = splitLinea[0]                     # '21/2/2021 11:27 a. m.'
    splitFechaHora = FechaHora.split(' ')   
    Fecha = splitFechaHora[0]                     # '21/2/2021'
    Hora = ' '.join(splitFechaHora[1:])           # '11:27 a. m.'
    Mensaje = ' '.join(splitLinea[1:])            # 'Sandro: Todos debemos aprender a analizar datos'
    if EncontrarMiembro(Mensaje): 
        splitMensaje = Mensaje.split(': ')      
        Miembro = splitMensaje[0]                 # 'Sandro' 
        Mensaje = ' '.join(splitMensaje[1:])      # 'Todos debemos aprender a analizar datos'
    else:
        Miembro = None
    return Fecha, Hora, Miembro, Mensaje


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
    # Intentamos convertir la fecha (añado dayfirst=True por si acaso)
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
        return [{"hour": f"{i}h", "messages": 0} for i in range(24)]
    
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
        resultado.append({"hour": f"{i}h", "messages": int(promedio)})
    
    return resultado

def obtener_dias_con_mas_mensajes(df: pd.DataFrame):
    if df.empty:
        return []
    
    # Filtramos mensajes del sistema (sin miembro asignado)
    df_filtrado = df[df['Miembro'].notna()].copy()
    
    # Contamos cuántos mensajes hubo por cada fecha
    conteo_por_dia = df_filtrado.groupby('Fecha').size().reset_index(name='cantidad_mensajes')
    
    # Ordenamos de mayor a menor
    conteo_por_dia = conteo_por_dia.sort_values('cantidad_mensajes', ascending=False)
    
    # Convertimos a lista de diccionarios para devolver como JSON
    return conteo_por_dia.to_dict(orient='records')