import React from "react";

const StudentForm = () => {
  return (
    <div>
      <h2>Ingreso de Estudiantes</h2>
      <form className="form-container">
        <label>
          First Name:
          <input type="text" name="firstName" />
        </label>
        <label>
          Last Name:
          <input type="text" name="lastName" />
        </label>
        <label>
          UID:
          <input type="text" name="uid" />
        </label>
        <label>
          Model:
          <input type="text" name="model" />
        </label>
      </form>
    </div>
  );
};

export default StudentForm;