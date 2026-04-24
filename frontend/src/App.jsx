import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import './css/App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Cuando el usuario esté en la raíz (/), muestra el componente Home */}
        <Route path="/" element={<Home />} />
        
        {/* Aquí podrías agregar más rutas fácilmente */}
        {/* <Route path="/dashboard" element={<Dashboard />} /> */}
      </Routes>
    </BrowserRouter>
  )
}

export default App