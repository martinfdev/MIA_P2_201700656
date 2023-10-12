import { Route, Routes } from 'react-router-dom'

//pages
import Home from './pages/Home'
import Login from './pages/Login'
import Reports from './pages/Reports'
import NotFound from './pages/NotFound'

function App() {
  return (
      <div>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/*" element={<NotFound />} />
            <Route path="/home" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
      </div>
  )
}
export default App
