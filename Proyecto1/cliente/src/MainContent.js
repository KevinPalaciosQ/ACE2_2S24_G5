import React from "react";
import StudentForm from "./StudentForm";
import BalanceManagement from "./BalanceManagement";
import ParkingManagement from "./ParkingManagement";

const MainContent = ({ selectedSection }) => {
  return (
    <div className="main-content">
      {selectedSection === "Ingreso de Estudiantes" && <StudentForm />}
      {selectedSection === "Administración de Saldos" && <BalanceManagement />}
      {selectedSection === "Administración de Parqueos" && <ParkingManagement />}
    </div>
  );
};

export default MainContent;
