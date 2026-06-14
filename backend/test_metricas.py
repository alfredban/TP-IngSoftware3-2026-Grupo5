import json
import pandas as pd
from logic import (
    obtener_ranking_mensajes, 
    emogiMasUsado, 
    obtener_mensajes_por_hora, 
    obtener_mensajes_por_dia_semana, 
    obtener_frecuencia_palabras
)

def imprimir_resultado(resultado):
    """
    Función auxiliar para imprimir resultados de forma compacta y legible.
    Mantiene la estructura de lista/json, pero con los objetos en una sola línea.
    """
    # Si la métrica devuelve un DataFrame, lo convertimos a lista de diccionarios
    if isinstance(resultado, pd.DataFrame):
        resultado = resultado.to_dict(orient='records')
        
    if isinstance(resultado, list):
        if not resultado:
            print("[]")
        else:
            print("[")
            for i, item in enumerate(resultado):
                line = json.dumps(item, ensure_ascii=False)
                print(f"  {line}," if i < len(resultado) - 1 else f"  {line}")
            print("]")
    elif isinstance(resultado, dict):
        print(json.dumps(resultado, ensure_ascii=False))
    else:
        print(resultado)

# =====================================================================
# EJECUCIÓN DE LAS PRUEBAS
# =====================================================================

def test_ranking_mensajes():
    print("\n" + "="*50)
    print("--- 1. PRUEBA: RANKING DE MENSAJES ---")
    
    # Caso 1: Conteo normal y empate
    df_ideal = pd.DataFrame([
        {"Miembro": "Juan", "Mensaje": "Hola"},
        {"Miembro": "Ana", "Mensaje": "Hola"},
        {"Miembro": "Juan", "Mensaje": "Chau"},
        {"Miembro": "Ana", "Mensaje": "Chau"},
        {"Miembro": "Pedro", "Mensaje": "Hola"}
    ])
    print("\nCaso 1 - Ideal y Empate")
    print("Esperado: Juan (2), Ana (2), Pedro (1)")
    print("Resultado:")
    imprimir_resultado(obtener_ranking_mensajes(df_ideal))

    # Caso 2: Ignorar mensajes de sistema
    df_sistema = pd.DataFrame([
        {"Miembro": "Juan", "Mensaje": "Hola"},
        {"Miembro": None, "Mensaje": "Juan creó el grupo"}
    ])
    print("\nCaso 2 - Ignorar Sistema")
    print("Esperado: Solo Juan con 1. 'None' debe ser ignorado")
    print("Resultado:")
    imprimir_resultado(obtener_ranking_mensajes(df_sistema))
    
    # Caso 3: Chat Vacío
    df_vacio = pd.DataFrame(columns=["Fecha", "Hora", "Miembro", "Mensaje"])
    print("\nCaso 3 - Chat Vacío")
    print("Esperado: DataFrame vacío")
    print("Resultado:")
    imprimir_resultado(obtener_ranking_mensajes(df_vacio))


def test_emoji_mas_usado():
    print("\n" + "="*50)
    print("--- 2. PRUEBA: EMOJI MÁS USADO ---")
    
    # Caso 1: Múltiples emojis
    df_ideal = pd.DataFrame([
        {"Mensaje": "Hola 👍"},
        {"Mensaje": "Jaja 🤣"},
        {"Mensaje": "Muy bueno 🤣🤣"}
    ])
    print("\nCaso 1 - Múltiples Emojis")
    print("Esperado: {'emoji': '🤣', 'cantidad': 3}")
    print("Resultado:")
    imprimir_resultado(emogiMasUsado(df_ideal))

    # Caso 2: Sin emojis
    df_sin = pd.DataFrame([
        {"Mensaje": "Hola a todos"},
        {"Mensaje": "Como andan"}
    ])
    print("\nCaso 2 - Sin emojis")
    print("Esperado: {'emoji': None, 'cantidad': 0}")
    print("Resultado:")
    imprimir_resultado(emogiMasUsado(df_sin))

    # Caso 3: Emoji con modificador (tono de piel)
    df_mod = pd.DataFrame([
        {"Mensaje": "Excelente 👍🏽"},
    ])
    print("\nCaso 3 - Modificador")
    print("Esperado: {'emoji': '👍🏽', 'cantidad': 1}")
    print("Resultado:")
    imprimir_resultado(emogiMasUsado(df_mod))


def test_mensajes_por_hora():
    print("\n" + "="*50)
    print("--- 3. PRUEBA: MENSAJES POR HORA ---")

    # Caso 1: Distribución normal
    df_ideal = pd.DataFrame([
        {"Fecha": "01/01/2026", "Hora": "14:00"},
        {"Fecha": "01/01/2026", "Hora": "14:30"},
        {"Fecha": "01/01/2026", "Hora": "09:15"}
    ])
    print("\nCaso 1 - Distribución Normal")
    print("Esperado: 14h con 2 msj, 9h con 1 msj")
    print("Resultado:")
    imprimir_resultado(obtener_mensajes_por_hora(df_ideal))

    # Caso 2: Confusión AM/PM vs 24hs
    df_ampm = pd.DataFrame([
        {"Fecha": "01/01/2026", "Hora": "12:15 a. m."},
        {"Fecha": "01/01/2026", "Hora": "12:15 p. m."}
    ])
    print("\nCaso 2 - AM/PM")
    print("Esperado: 0h con 1 msj, 12h con 1 msj")
    print("Resultado:")
    imprimir_resultado(obtener_mensajes_por_hora(df_ampm))

    # Caso 3: Integridad y Orden (Gráficos)
    df_vacio = pd.DataFrame(columns=["Fecha", "Hora", "Miembro", "Mensaje"])
    print("\nCaso 3 - Integridad y Orden (Gráficos)")
    print("Esperado: Array de 24 elementos obligatorios (0h a 23h) ordenados, con cantidad 0.")
    print("Resultado:")
    imprimir_resultado(obtener_mensajes_por_hora(df_vacio))


def test_mensajes_por_dia_semana():
    print("\n" + "="*50)
    print("--- 4. PRUEBA: MENSAJES POR DÍA DE LA SEMANA ---")

    # Caso 1: Agrupación normal
    # Se considera: 01/06/2026 fue Lunes, 02/06/2026 fue Martes
    df_ideal = pd.DataFrame([
        {"Fecha": "01/06/2026", "Miembro": "A"},
        {"Fecha": "01/06/2026", "Miembro": "A"},
        {"Fecha": "02/06/2026", "Miembro": "B"}
    ])
    print("\nCaso 1 - Agrupación Semanal")
    print("Esperado: Lunes 2, Martes 1")
    print("Resultado:")
    imprimir_resultado(obtener_mensajes_por_dia_semana(df_ideal))

    # Caso 2: Ignorar Sistema
    df_sistema = pd.DataFrame([
        {"Fecha": "01/06/2026", "Miembro": "A"},
        {"Fecha": "02/06/2026", "Miembro": None} # Mensaje del sistema el Martes
    ])
    print("\nCaso 2 - Ignorar Sistema")
    print("Esperado: Solo reporta Lunes 1, omite Martes")
    print("Resultado:")
    imprimir_resultado(obtener_mensajes_por_dia_semana(df_sistema))

    # Caso 3: Integridad y Orden (Gráficos)
    df_dias = pd.DataFrame([{"Fecha": "01/06/2026", "Miembro": "A"}]) # Solo Lunes
    print("\nCaso 3 - Integridad y Orden (Gráficos)")
    print("Esperado: Array de 7 elementos ordenados (Lunes a Domingo). Lunes en 1, el resto en 0.")
    print("Resultado:")
    imprimir_resultado(obtener_mensajes_por_dia_semana(df_dias))


def test_frecuencia_palabras():
    print("\n" + "="*50)
    print("--- 5. PRUEBA: NUBE DE PALABRAS ---")

    # Caso 1: Limpieza básica y Case Insensitive
    df_ideal = pd.DataFrame([
        {"Mensaje": "Perro gato Perro"}
    ])
    print("\nCaso 1 - Limpieza básica")
    print("Esperado: [{'word': 'perro', 'frecuency': 2}, {'word': 'gato', 'frecuency': 1}]")
    print("Resultado:")
    imprimir_resultado(obtener_frecuencia_palabras(df_ideal))

    # Caso 2: Ignorar URL, menciones y stop words
    df_borde = pd.DataFrame([
        {"Mensaje": "El perro de https://google.com ladra a @juan"}
    ])
    print("\nCaso 2 - Filtros (Ignorar menciones y URLs)")
    print("Esperado: Solo deben contabilizarse palabras útiles como 'perro' y 'ladra'")
    print("Resultado:")
    imprimir_resultado(obtener_frecuencia_palabras(df_borde))


# =====================================================================
# LANZADOR DE PRUEBAS
# =====================================================================
if __name__ == "__main__":
    print("INICIANDO BATERÍA DE PRUEBAS DE MÉTRICAS...")
    test_ranking_mensajes()
    test_emoji_mas_usado()
    test_mensajes_por_hora()
    test_mensajes_por_dia_semana()
    test_frecuencia_palabras()
