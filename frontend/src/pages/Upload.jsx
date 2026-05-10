import { useState } from 'react'

function Upload() {
  const [archivo, setArchivo] = useState(null)
  const [respuesta, setRespuesta] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)

  const handleSeleccion = (e) => {
    setArchivo(e.target.files[0])
    setRespuesta(null)
    setError(null)
  }

  const handleSubir = async () => {
    if (!archivo) return

    setCargando(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', archivo)

    try {
      const res = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      setRespuesta(data)
    } catch (err) {
      setError('Error al conectar con el servidor')
    } finally {
      setCargando(false)
    }
  }

  return (
    <div>
      <h2>Cargar chat de WhatsApp</h2>

      <input type="file" accept=".txt" onChange={handleSeleccion} />

      <button onClick={handleSubir} disabled={!archivo || cargando}>
        {cargando ? 'Subiendo...' : 'Subir archivo'}
      </button>

      {respuesta && (
        <div>
          <p> {respuesta.mensaje}</p>
          <p> Archivo: {respuesta.nombre_archivo}</p>
          <p> Tamaño: {respuesta.tamaño_bytes} bytes</p>
          <p> Líneas: {respuesta.lineas}</p>
        </div>
      )}

      {error && <p> {error}</p>}
    </div>
  )
}

export default Upload