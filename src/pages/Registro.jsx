import { useState } from "react";
import { useNavigate } from "react-router-dom";

const API_URL = "http://localhost:8000";

function Registro() {
  const [nombre, setNombre] = useState("");
  const [codigo, setCodigo] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Validaciones básicas
    if (!nombre || !codigo || !password) {
      setError("Nombre, código y contraseña son obligatorios");
      setLoading(false);
      return;
    }

    // Generar email a partir del código
    const email = `${codigo}@alumnos.udg.mx`;

    // Datos exactos que espera el backend
    const usuarioData = {
      nombre: nombre,
      codigo: codigo,
      email: email,
      password: password
      // 'rol' lo asigna el backend por defecto como "estudiante"
    };

    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(usuarioData),
      });

      const data = await response.json();

      if (response.ok) {
        alert("Registro exitoso. Ahora puedes iniciar sesión.");
        navigate("/login");
      } else {
        // Mostrar el error detallado que devuelve el backend
        console.error("Error del backend:", data);
        if (data.detail && Array.isArray(data.detail)) {
          // Si es un error de validación de Pydantic
          const mensajes = data.detail.map(err => err.msg).join(", ");
          setError(mensajes);
        } else {
          setError(data.detail || "Error en el registro");
        }
      }
    } catch (err) {
      setError("Error de conexión con el servidor");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>Registro de Alumno</h1>
        
        {/* Mostrar errores de forma segura */}
        {error && (
          <div style={{ color: 'red', marginBottom: '15px', padding: '10px', backgroundColor: '#ffeeee', borderRadius: '4px' }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Nombre completo"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
            disabled={loading}
          />
          <input
            type="text"
            placeholder="Código (ej. 2213522292)"
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
            required
            disabled={loading}
          />
          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? "Registrando..." : "Registrarse"}
          </button>
        </form>

        <p style={{ marginTop: '15px' }}>
          ¿Ya tienes cuenta? <a href="/login">Inicia sesión</a>
        </p>
      </div>
    </div>
  );
}

export default Registro;