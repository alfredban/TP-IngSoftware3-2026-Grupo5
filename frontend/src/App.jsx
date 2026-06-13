import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Upload from './pages/Upload'
import './css/App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Cuando el usuario esté en la raíz (/), muestra el componente Home */}
        <Route path="/" element={<Home />} />
        
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App