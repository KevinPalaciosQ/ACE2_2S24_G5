import React from "react";
import './App.css';
import { FaUser, FaMoneyBill, FaCar } from "react-icons/fa"; // Ejemplo con react-icons

const Sidebar = ({ setSelectedSection }) => {
  return (
    <div className="sidebar">
      <span onClick={() => setSelectedSection("Ingreso de Estudiantes")} className="menu-item">
        <FaUser /> Ingreso de Estudiantes
      </span>
      <span onClick={() => setSelectedSection("Administración de Saldos")} className="menu-item">
        <FaMoneyBill /> Administración de Saldos
      </span>
      <span onClick={() => setSelectedSection("Administración de Parqueos")} className="menu-item">
        <FaCar /> Administración de Parqueos
      </span>
    </div>
  );
};

export default Sidebar;
