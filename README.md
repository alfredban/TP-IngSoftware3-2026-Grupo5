# 📊 Análisis de Chats de WhatsApp - Grupo 5

## 📝 Descripción
Proyecto desarrollado para la materia **Ingeniería de Software 3 (Universidad Nacional de Lanús, 2026)**. Consiste en una aplicación web que permite subir un archivo de chat exportado de WhatsApp (`.txt` o `.zip`) y genera un dashboard interactivo con métricas y análisis de datos, incluyendo:
- 🏆 Persona que más mensajes envió.
- 😀 Emoji más utilizado.
- 🕒 Franja horaria con mayor actividad.
- 📅 Días con mayor cantidad de mensajes.
- ☁️ Nube de palabras más utilizadas.

## 🛠️ Tecnologías Utilizadas
- **Backend**: Python, FastAPI, Pandas.
- **Frontend**: React, Vite, Chart.js.

## 🧠 Decisiones Técnicas y Arquitectura
Para cumplir con los criterios de evaluación del trabajo práctico, el sistema fue diseñado con las siguientes consideraciones:
- **Arquitectura Desacoplada:** Se separó el proyecto en Frontend y Backend. Esto permite que el backend se especialice puramente en el procesamiento pesado de datos, mientras que el frontend se dedique exclusivamente a la visualización interactiva.
- **Procesamiento de Datos (Pandas):** Se eligió Pandas en el backend por su alta eficiencia y facilidad para manejar series temporales, agrupaciones complejas y manipulación de texto (esencial para los cálculos de métricas como franjas horarias y días de la semana).
- **Formatos Soportados:** El sistema está preparado para procesar el formato estándar de exportación de WhatsApp (`.txt` y su variante en `.zip`). El parseo se realiza asumiendo un formato típico de exportación sin alteraciones manuales.

## 🚀 Instalación y Ejecución

El proyecto está dividido en dos partes independientes: el Backend (API) y el Frontend (Interfaz). Necesitarás tener instalados **Python** y **Node.js** en tu computadora.

### ⚙️ 1. Levantar el Backend
El backend se encarga de procesar el archivo de texto y calcular las métricas.

1. Abre una terminal y dirígete a la carpeta del backend:
   ```bash
   cd backend
   ```
2. *(Opcional pero recomendado)* Crea y activa un entorno virtual.
3. Instala las dependencias (si aplica).
4. Ejecuta el servidor:
   ```bash
   python -m uvicorn main:app --reload
   ```
5. El backend estará corriendo en: `http://localhost:8000/`
6. **Documentación de la API (Swagger UI):** Puedes ver y probar los endpoints interactivos ingresando a `http://127.0.0.1:8000/docs` en tu navegador.

### 💻 2. Levantar el Frontend
El frontend es la interfaz gráfica donde el usuario interactúa y ve los gráficos.

1. Abre una **nueva** terminal y dirígete a la carpeta del frontend:
   ```bash
   cd frontend
   ```
2. Instala los paquetes de Node:
   ```bash
   npm install
   ```
3. Levanta el entorno de desarrollo:
   ```bash
   npm run dev
   ```
4. La interfaz estará disponible en tu navegador en: `http://localhost:5173/`

---
💡 **Nota:** Para detener cualquiera de los dos servidores, simplemente presiona `Ctrl + C` en la terminal correspondiente.
