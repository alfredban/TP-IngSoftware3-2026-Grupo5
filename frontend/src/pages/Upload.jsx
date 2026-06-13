import { useState } from 'react'

function Upload() {
  const [archivo, setArchivo] = useState(null)
  const [respuesta, setRespuesta] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)

  const handleSubir = async () => {
    if (!archivo) return
    setCargando(true)
    setError(null)
    setRespuesta(null)

    const formData = new FormData()
    formData.append('file', archivo)

    try {
      // Usamos 127.0.0.1 para evitar demoras de resolución de DNS en local
      const res = await fetch('http://127.0.0.1:8000/api/upload', {
        method: 'POST',
        body: formData,
      })
      
      const data = await res.json()

      if (!res.ok) {
        setError(data.detail || 'Error en la validación')
      } else {
        setRespuesta(data)
      }
    } catch (err) {
      setError('Error de conexión. Asegurate de que el Backend esté corriendo.')
    } finally {
      setCargando(false)
    }
  }

  return (
    <div style={{ maxWidth: '500px', margin: '50px auto', fontFamily: 'sans-serif', textAlign: 'center' }}>
      <h2 style={{ color: '#075E54' }}>Validar Formato de Chat</h2>
      
      <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '10px' }}>
        <input type="file" accept=".txt" onChange={(e) => setArchivo(e.target.files[0])} />
        <br /><br />
        <button onClick={handleSubir} disabled={!archivo || cargando} style={{
          padding: '10px 20px', backgroundColor: '#25D366', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer'
        }}>
          {cargando ? 'Validando...' : 'Subir Archivo'}
        </button>
      </div>

      {error && (
        <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#ffd7d7', color: '#a00', borderRadius: '5px' }}>
          <strong>❌ {error}</strong>
        </div>
      )}

      {respuesta && (
        <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#d7ffd7', color: '#007a00', borderRadius: '5px' }}>
          <strong>✅ {respuesta.mensaje}</strong>
          <p>Archivo: {respuesta.nombre_archivo}</p>
          <p>Líneas: {respuesta.lineas}</p>
        </div>
      )}
    </div>
  )
}

export default Upload