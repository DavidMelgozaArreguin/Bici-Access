import { useState } from "react";
import { useNavigate } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Registro() {
  // Campos usuario
  const [nombre, setNombre] = useState("");
  const [codigo, setCodigo] = useState("");
  const [password, setPassword] = useState("");
  // Campos vehículo (bicicleta)
  const [marca, setMarca] = useState("");
  const [modelo, setModelo] = useState("");
  const [color, setColor] = useState("");
  const [serial, setSerial] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    localStorage.removeItem("token"); // Limpia cualquier sesion anterior
    e.preventDefault();
    setLoading(true);
    setError("");

    // Validaciones básicas
    if (!nombre || !codigo || !password) {
      setError("Nombre, código y contraseña son obligatorios");
      setLoading(false);
      return;
    }

    // Validar campos de bicicleta (opcionales, pero si se rellena alguno, todos?)
    // Por simplicidad, permitimos que los campos de bici sean opcionales.
    // Si se quiere obligar, descomentar la siguiente línea:
    // if (!marca || !modelo || !color || !serial) {
    //   setError("Datos de bicicleta incompletos");
    //   setLoading(false);
    //   return;
    // }

    const email = `${codigo}@alumnos.udg.mx`;

    const usuarioData = {
      nombre,
      codigo,
      email,
      password,
    };

    try {
      // 1. Registrar usuario
      const registerRes = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(usuarioData),
      });
      const registerData = await registerRes.json();

      if (!registerRes.ok) {
        const mensaje = registerData.detail?.[0]?.msg || registerData.detail || "Error en registro";
        throw new Error(mensaje);
      }

      // 2. Login automático para obtener token
      const loginRes = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const loginData = await loginRes.json();

      if (!loginRes.ok) {
        throw new Error("No se pudo iniciar sesión automáticamente");
      }
      const token = loginData.access_token;

      // 3. Registrar bicicleta si se proporcionaron datos
      if (marca || modelo || color || serial) {
        const bicicletaData = { marca, modelo, color, serial };
        const biciRes = await fetch(`${API_URL}/bicicletas/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(bicicletaData),
        });
        if (!biciRes.ok) {
          const biciError = await biciRes.json();
          console.warn("Error registrando bicicleta:", biciError);
          // No detenemos el flujo, solo advertimos
          alert("Usuario registrado, pero hubo un error al guardar la bicicleta: " + (biciError.detail || "Error desconocido"));
        }
      }

      // 4. Guardar token en localStorage para mantener sesión
      localStorage.setItem("token", token);
      alert("Registro exitoso. Serás redirigido al login.");
      navigate("/login");
    } catch (err) {
      setError(err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>Registro de Alumno</h1>

        {error && (
          <div style={{ color: 'red', marginBottom: '15px', padding: '10px', backgroundColor: '#ffeeee', borderRadius: '4px' }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <h3>Datos personales</h3>
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

          <hr />
          <h3>Datos de tu bicicleta (opcional)</h3>
          <input
            type="text"
            placeholder="Marca"
            value={marca}
            onChange={(e) => setMarca(e.target.value)}
            disabled={loading}
          />
          <input
            type="text"
            placeholder="Modelo"
            value={modelo}
            onChange={(e) => setModelo(e.target.value)}
            disabled={loading}
          />
          <input
            type="text"
            placeholder="Color"
            value={color}
            onChange={(e) => setColor(e.target.value)}
            disabled={loading}
          />
          <input
            type="text"
            placeholder="Número de serie"
            value={serial}
            onChange={(e) => setSerial(e.target.value)}
            disabled={loading}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Procesando..." : "Registrarse"}
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