import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styless/Login.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Login() {

  const [codigo, setCodigo] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const iniciarSesion = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError("");

  const email = `${codigo}@alumnos.udg.mx`;

  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    // 1. Extraemos los datos UNA SOLA VEZ
    const data = await response.json();
    console.log("DATOS DEL BACKEND:", data);

    if (response.ok) {
        // 2. Verificamos que el token venga en 'access_token'
        if (data.access_token) {
            localStorage.setItem("access_token", data.access_token);
            console.log("TOKEN GUARDADO EN STORAGE ✅");
            
            // 3. Redirigimos
            navigate("/perfil");
        } else {
            setError("El servidor no envió un access_token");
        }
    } else {
        setError(data.detail || "Credenciales incorrectas");
    }
  } catch (err) {
    console.error("Error de captura:", err);
    setError("Error de conexión con el servidor");
  } finally {
    setLoading(false);
  }
};
 
  return (

    <div className="login-container">

      <div className="login-box">

        <h1>BICI-ACCESS</h1>

        {error && (
          <div style={{ color: "red", marginBottom: "10px" }}>
            {error}
          </div>
        )}

        <form onSubmit={iniciarSesion}>
          <input
            type="text"
            placeholder="Código"
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" disabled={loading}>

            {loading ? "Entrando..." : "Iniciar sesión"}

          </button>

        </form>

        <p>

          ¿No tienes cuenta? <a href="/registro">Regístrate</a>

        </p>

      </div>

    </div>

  );

}

export default Login;