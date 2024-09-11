import React from "react";
import './StudentForm.css';

const StudentForm = () => {
  return (
    <div className="card-container">
      <div className="student-form-card">
        <div className="student-form-content">
          <div className="photo-container">
            <img
              src="https://via.placeholder.com/150" // URL de la imagen (puedes reemplazarla con la foto deseada)
              alt="Student"
              className="student-photo"
            />
          </div>
          <div className="form-content">
            <h2>Ingreso de Estudiantes</h2>
            <form className="form-container">
              <label>
                First Name:
                <input type="text" name="firstName" disabled />
              </label>
              <label>
                Last Name:
                <input type="text" name="lastName" disabled />
              </label>
              <label>
                UID:
                <input type="text" name="uid" disabled />
              </label>
              <label>
                Model:
                <input type="text" name="model" disabled />
              </label>
            </form>
            <div className="form-buttons">
              <button type="button" className="prev-button">Anterior</button>
              <button type="button" className="next-button">Siguiente</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentForm;
