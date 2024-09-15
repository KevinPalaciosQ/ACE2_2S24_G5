import React, { useState } from "react";
import "./Login.css";

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    if (email === "administrador@administrador" && password === "administrador") {
      console.log("Email:", email);
      console.log("Password:", password);
      alert("Inicio de sesión exitoso");
      onLogin();  // Llama a la función para cambiar el estado y redirigir
    } else {
      alert("Credenciales incorrectas");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Iniciar Sesión</h2>
        <form onSubmit={handleLogin}>
          <div className="input-group">
            <label htmlFor="email">Correo electrónico</label>
            <input
              type="email"
              id="email"
              placeholder="administrador@administrador"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Contraseña</label>
            <input
              type="password"
              id="password"
              placeholder="administrador"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button className="login-btn" type="submit">Ingresar</button>
        </form>
      </div>
    </div>
  );
};

export default Login;
