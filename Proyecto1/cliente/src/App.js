import React, { useState } from "react";
import Sidebar from "./Sidebar";  // Asegúrate de que se llame "Sidebar"
import MainContent from "./MainContent";
import "./App.css";

function App() {
  const [selectedSection, setSelectedSection] = useState("Ingreso de Estudiantes");

  return (
    <div className="container">
      <Sidebar setSelectedSection={setSelectedSection} />
      <MainContent selectedSection={selectedSection} />
    </div>
  );
}

export default App;
