import React, { useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import Sidebar from "./Sidebar";
import MainContent from "./MainContent";
import Login from "./Login";
import "./App.css";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [selectedSection, setSelectedSection] = useState("Ingreso de Estudiantes");
  const navigate = useNavigate();  // Hook para la navegación

  const handleLogin = () => {
    setIsAuthenticated(true);
    navigate("/main");  // Redirige a la ruta de contenido principal
  };

  return (
    <div className="container">
      <Routes>
        <Route path="/" element={<Login onLogin={handleLogin} />} />
        <Route path="/main" element={isAuthenticated ? (
          <>
            <Sidebar setSelectedSection={setSelectedSection} />
            <MainContent selectedSection={selectedSection} />
          </>
        ) : (
          <Login onLogin={handleLogin} />
        )} />
      </Routes>
    </div>
  );
}

export default App;
