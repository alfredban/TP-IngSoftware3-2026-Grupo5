import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Dashboard, Upload } from './pages'
import './index.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Cuando el usuario esté en la raíz (/), redirige al usuario a /upload por defecto */}
        <Route path="/" element={<Navigate to="/upload" replace />} />

        {/* Rutas de la aplicación */}
        <Route path="/upload" element={<Upload />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App