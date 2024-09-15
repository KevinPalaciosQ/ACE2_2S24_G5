import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';  // Importa BrowserRouter
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <Router>  {/* Envuelve la aplicación con BrowserRouter */}
      <App />
    </Router>
  </React.StrictMode>
);

reportWebVitals();

