import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import LandingPage from "./components/LandingPage"
import ChatPage from "./components/ChatPage"
import "./index.css"

function App() {
  return (
    <Router>
      <Routes>
        {/* Page d'accueil / Site vitrine */}
        <Route path="/" element={<LandingPage />} />

        {/* Page du Chat */}
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </Router>
  )
}

export default App