import React, { useState } from "react";
import "./Login.css";
import { FaUser, FaLock } from "react-icons/fa";

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    if (username === "administrador@administrador" && password === "administrador") {
      console.log("Username:", username);
      console.log("Password:", password);
      alert("Inicio de sesión exitoso");
      onLogin(); // Realización del login
    } else {
      alert("Credenciales incorrectas");
    }
  };

  return (
    <div className="wrapper">
      <form onSubmit={handleLogin}>
        <h1>Login</h1>
        <div className="input-box">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <FaUser className="icon" />
        </div>

        <div className="input-box">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <FaLock className="icon" />
        </div>

        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
